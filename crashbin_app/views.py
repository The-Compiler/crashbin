import logging
import typing

import attr
from django import urls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.core import mail

from crashbin_app import utils
from .models import Report, Bin, NoteMessage, OutgoingMessage, Message, Label
from .forms import BinForm, ReportReplyForm, LabelForm


@login_required
def home(request: HttpRequest) -> HttpResponse:
    user = request.user  # type: ignore
    data = {
        'bins': Bin.objects.order_by('created_at'),
        'reports': Report.objects,
        'maintained_bins': Bin.objects.filter(maintainers=user),
        'subscribed_bins': Bin.objects.filter(subscribers=user),
    }
    return render(request, 'crashbin_app/home.html', data)


@login_required
def report_list(request: HttpRequest) -> HttpResponse:
    reports = Report.objects.order_by('created_at')
    if 'q' in request.GET:
        query = request.GET['q']
        reports = reports.filter(title__icontains=query)
    else:
        query = None

    return render(request,
                  'crashbin_app/reports.html',
                  {'reports': reports, 'query': query})


@login_required
def report_detail(request: HttpRequest, pk: int) -> HttpResponse:
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'crashbin_app/report_detail.html',
                  {'report': report})


@login_required
@require_POST
def report_reply(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user  # type: ignore
    report = get_object_or_404(Report, pk=pk)

    form = ReportReplyForm(request.POST)
    if not form.is_valid():
        logging.error("Invalid reply POST: %s", form.errors)
        return HttpResponseBadRequest("Invalid form data")

    typ = form.cleaned_data['typ']
    text = form.cleaned_data['text']
    msg: Message

    if typ == 'Reply':
        msg = OutgoingMessage.objects.create(text=text, author=user, report=report)
        mail.send_mail(
            subject=utils.config.EMAIL['outgoing_subject'].format(report.id),
            message=text,
            from_email=utils.config.EMAIL['outgoing_address'],
            recipient_list=[report.email],
            fail_silently=False,
        )
        fragment = 'reply-{}'.format(msg.id)
    elif typ == 'Note':
        msg = NoteMessage.objects.create(text=text, author=user, report=report)
        fragment = 'note-{}'.format(msg.id)
    else:
        assert False, typ

    url = urls.reverse('report_detail', kwargs={'pk': pk})
    return redirect('{}#{}'.format(url, fragment))


@login_required
def bin_list(request: HttpRequest) -> HttpResponse:
    bins = Bin.objects.order_by('created_at')
    if 'q' in request.GET:
        query = request.GET['q']
        bins = bins.filter(name__icontains=query)
    else:
        query = None

    return render(request,
                  'crashbin_app/bins.html',
                  {'bins': bins, 'query': query})


@login_required
def bin_detail(request: HttpRequest, pk: int) -> HttpResponse:
    bin_obj = get_object_or_404(Bin, pk=pk)
    return render(request, 'crashbin_app/bin_detail.html',
                  {'bin': bin_obj})


@login_required
def bin_new_edit(request: HttpRequest, pk: int = None) -> HttpResponse:
    if request.method == 'POST':
        form = BinForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid form data")
        bin_obj = form.save()
        return redirect('bin_detail', pk=bin_obj.pk)
    else:
        if pk is None:
            form = BinForm()
        else:
            bin_obj = get_object_or_404(Bin, pk=pk)
            form = BinForm(instance=bin_obj)
    return render(request, 'crashbin_app/form.html',
                  {'title': 'Edit bin' if pk else 'New bin', 'form': form, 'menu': 'bins'})


def label_list(request: HttpRequest) -> HttpResponse:
    labels = Label.objects.order_by('created_at')
    if 'q' in request.GET:
        query = request.GET['q']
        labels = labels.filter(name__icontains=query)
    else:
        query = None

    return render(request,
                  'crashbin_app/labels.html',
                  {'labels': labels, 'query': query})


@login_required
def label_detail(request: HttpRequest, pk: int) -> HttpResponse:
    label_obj = get_object_or_404(Label, pk=pk)
    return render(request, 'crashbin_app/label_detail.html',
                  {'label': label_obj})


@login_required
def label_new_edit(request: HttpRequest, pk: int = None) -> HttpResponse:
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid form data")
        label_obj = form.save()
        return redirect('label_detail', pk=label_obj.pk)
    else:
        if pk is None:
            form = LabelForm()
        else:
            label_obj = get_object_or_404(Label, pk=pk)
            form = LabelForm(instance=label_obj)
    return render(request, 'crashbin_app/form.html',
                  {'title': 'Edit label' if pk else 'New label', 'form': form, 'menu': 'labels'})


@login_required
@require_POST
def bin_subscribe(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user  # type: ignore
    bin_obj: Bin = Bin.objects.get(id=pk)
    if user in bin_obj.subscribers.all():
        bin_obj.subscribers.remove(user)
    else:
        bin_obj.subscribers.add(user)
    return HttpResponse()


@login_required
def settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    if request.method == 'GET':
        return _get_settings(request, pk, setting)
    if request.method == 'POST':
        return _set_settings(request, pk, setting)
    return HttpResponseBadRequest("Invalid method request")


@attr.s
class _ButtonInfo:

    text: str = attr.ib()
    view: str = attr.ib()


def _get_settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    Element = typing.Union[User, Label, Bin]
    all_elements: QuerySet
    selected_elements: typing.Iterable[Element]
    title: str
    new_button: typing.Optional[_ButtonInfo] = None

    if setting == 'maintainer':
        bin_obj = get_object_or_404(Bin, pk=pk)
        all_elements = User.objects.order_by('id')
        selected_elements = bin_obj.maintainers.all()
        title = 'Maintainers for {}'.format(bin_obj)
    elif setting == 'label':
        all_elements = Label.objects.order_by('created_at')
        new_button = _ButtonInfo("New label", 'label_new_edit')
        if request.path.startswith('/bin/'):
            bin_obj = get_object_or_404(Bin, pk=pk)
            selected_elements = bin_obj.labels.all()
            title = 'Labels for {}'.format(bin_obj)
        elif request.path.startswith('/report/'):
            report_obj = get_object_or_404(Report, pk=pk)
            selected_elements = report_obj.labels.all()
            title = 'Labels for {}'.format(report_obj)
        else:
            assert False, request.path
    elif setting == 'related':
        new_button = _ButtonInfo("New bin", 'bin_new_edit')
        bin_obj = get_object_or_404(Bin, pk=pk)
        all_elements = Bin.objects.exclude(id=pk)
        selected_elements = bin_obj.related_bins.all()
        title = 'Related to {}'.format(bin_obj)
    elif setting == 'assigned':
        new_button = _ButtonInfo("New bin", 'bin_new_edit')
        report_obj = get_object_or_404(Report, pk=pk)
        all_elements = Bin.objects.order_by('created_at')
        selected_elements = [report_obj.bin]
        title = 'Bin for {}'.format(report_obj)
    else:
        return HttpResponseBadRequest("Invalid setting request")

    return render(request, 'crashbin_app/set_settings.html',
                  {'pk': pk, 'setting': setting, 'all_elements': all_elements,
                   'selected_elements': selected_elements, 'title': title,
                   'new_button': new_button})


def _set_settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    element: typing.Union[Report, Bin]
    redirect_view: str
    query_list: typing.Sequence = request.POST.getlist(key=setting)

    if request.path.startswith('/bin/'):
        element = Bin.objects.get(id=pk)
        redirect_view = 'bin_detail'
    elif request.path.startswith('/report/'):
        element = Report.objects.get(id=pk)
        redirect_view = 'report_detail'
    else:
        return HttpResponseBadRequest("Invalid request")

    if setting == 'maintainer':
        assert isinstance(element, Bin)
        element.maintainers.clear()
        for maintainer in query_list:
            element.maintainers.add(User.objects.get(id=maintainer))
    elif setting == 'label':
        element.labels.clear()
        for label in query_list:
            element.labels.add(Label.objects.get(id=label))
    elif setting == 'related':
        assert isinstance(element, Bin)
        element.related_bins.clear()
        for related_bin in query_list:
            element.related_bins.add(Bin.objects.get(id=related_bin))
    elif setting == 'assigned':
        assert isinstance(element, Report)
        element.bin = Bin.objects.get(id=query_list[0])
        element.save()
    else:
        return HttpResponseBadRequest("Invalid setting request")
    return redirect(redirect_view, pk=pk)


@login_required
def search_dispatch(request: HttpRequest) -> HttpResponse:
    scope: str = request.GET['scope']
    if scope == 'Reports':
        return report_list(request)
    if scope == 'Bins':
        return bin_list(request)
    assert False, scope
    return None
