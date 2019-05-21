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
def set_settings(request: HttpRequest, pk: int, scope: str) -> HttpResponse:
    Element = typing.Union[User, Label, Bin]
    all_elements: QuerySet
    selected_elements: typing.Iterable[Element]
    visible_elements: typing.Iterable[Element]

    if scope == 'maintainer':
        all_elements = User.objects.order_by('id')
        selected_elements = get_object_or_404(Bin, pk=pk).maintainers.all()
    elif scope == 'label':
        all_elements = Label.objects.order_by('created_at')
        if 'bin' in request.path:
            selected_elements = get_object_or_404(Bin, pk=pk).labels.all()
        if 'report' in request.path:
            selected_elements = get_object_or_404(Report, pk=pk).labels.all()
    elif scope == 'related':
        all_elements = Bin.objects.exclude(id=pk)
        selected_elements = get_object_or_404(Bin, pk=pk).related_bins.all()
    elif scope == 'assigned':
        all_elements = Bin.objects.order_by('created_at')
        selected_elements = [get_object_or_404(Report, pk=pk).bin]
    else:
        return HttpResponseBadRequest("Invalid request")

    if 'q' in request.GET:
        query = request.GET['q']
        visible_elements = all_elements.filter(username__icontains=query).all()
    else:
        query = None
        visible_elements = all_elements
    return render(request, 'crashbin_app/set_settings.html',
                  {'pk': pk, 'scope': scope, 'query': query, 'all_elements': all_elements,
                   'selected_elements': selected_elements, 'visible_elements': visible_elements})


@login_required
def search_dispatch(request: HttpRequest) -> HttpResponse:
    scope: str = request.GET['scope']
    if scope == 'Reports':
        return report_list(request)
    if scope == 'Bins':
        return bin_list(request)
    assert False, scope
    return None
