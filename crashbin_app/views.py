import logging
import typing

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
from .forms import BinForm, ReportReplyForm


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
def bin_new(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BinForm(request.POST)
        if form.is_valid():
            bin_obj = form.save()
            return redirect('bin_detail', pk=bin_obj.pk)
    else:
        form = BinForm()
    return render(request, 'crashbin_app/bin_edit.html',
                  {'form': form})


@login_required
@require_POST
def bin_subscribe(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user  # type: ignore
    bin_obj: Bin = Bin.objects.get(id=pk)
    if user in bin_obj.subscribers.all():
        bin_obj.subscribers.remove(user)
    else:
        bin_obj.subscribers.add(user)
    return HttpResponse(status=200)


@login_required
def settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    if request.method == 'GET':
        return _get_settings(request, pk, setting)
    if request.method == 'POST':
        return _set_settings(request, pk, setting)
    return HttpResponseBadRequest("Invalid method request")


def _get_settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    Element = typing.Union[User, Label, Bin]
    all_elements: QuerySet
    selected_elements: typing.Iterable[Element]
    visible_elements: typing.Iterable[Element]
    title: str

    if setting == 'maintainer':
        bin_obj = get_object_or_404(Bin, pk=pk)
        all_elements = User.objects.order_by('id')
        selected_elements = bin_obj.maintainers.all()
        title = 'Maintainers for {}'.format(bin_obj)
    elif setting == 'label':
        all_elements = Label.objects.order_by('created_at')
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
        bin_obj = get_object_or_404(Bin, pk=pk)
        all_elements = Bin.objects.exclude(id=pk)
        selected_elements = bin_obj.related_bins.all()
        title = 'Related to {}'.format(bin_obj)
    elif setting == 'assigned':
        report_obj = get_object_or_404(Report, pk=pk)
        all_elements = Bin.objects.order_by('created_at')
        selected_elements = [report_obj.bin]
        title = 'Bin for {}'.format(report_obj)
    else:
        return HttpResponseBadRequest("Invalid setting request")

    if 'q' in request.GET:
        query = request.GET['q']
        if setting == 'maintainer':
            visible_elements = all_elements.filter(username__icontains=query).all()
        else:
            visible_elements = all_elements.filter(name__icontains=query).all()
    else:
        query = None
        visible_elements = all_elements
    return render(request, 'crashbin_app/set_settings.html',
                  {'pk': pk, 'setting': setting, 'query': query, 'all_elements': all_elements,
                   'selected_elements': selected_elements, 'visible_elements': visible_elements,
                   'title': title})


def _set_settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    element: typing.Union[Report, Bin]
    redirect_path: str
    query_list: typing.Sequence = request.POST.getlist(key=setting)

    if request.path.startswith('/bin/'):
        element = Bin.objects.get(id=pk)
        redirect_path = 'bin_detail'
    elif request.path.startswith('/report/'):
        element = Report.objects.get(id=pk)
        redirect_path = 'report_detail'
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
    return redirect(redirect_path, pk=pk)


@login_required
def search_dispatch(request: HttpRequest) -> HttpResponse:
    setting: str = request.GET['setting']
    if setting == 'Reports':
        return report_list(request)
    if setting == 'Bins':
        return bin_list(request)
    assert False, setting
    return None
