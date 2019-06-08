import logging

from django import urls
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from crashbin_app import utils
from crashbin_app.forms import ReportReplyForm
from crashbin_app.models import Report, Message, OutgoingMessage, NoteMessage


@login_required
def report_list(request: HttpRequest) -> HttpResponse:
    reports = Report.objects.all()
    if "q" in request.GET:
        query = request.GET["q"]
        reports = reports.filter(title__icontains=query)
    else:
        query = None

    return render(
        request, "crashbin_app/reports.html", {"reports": reports, "query": query}
    )


@login_required
def report_detail(request: HttpRequest, pk: int) -> HttpResponse:
    report = get_object_or_404(Report, pk=pk)
    return render(request, "crashbin_app/report_detail.html", {"report": report})


@login_required
@require_POST
def report_reply(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user  # type: ignore
    report = get_object_or_404(Report, pk=pk)

    form = ReportReplyForm(request.POST)
    if not form.is_valid():
        logging.error("Invalid reply POST: %s", form.errors)
        return HttpResponseBadRequest("Invalid form data")

    typ = form.cleaned_data["typ"]
    text = form.cleaned_data["text"]
    msg: Message

    if typ == "Reply":
        msg = OutgoingMessage.objects.create(text=text, author=user, report=report)
        mail.send_mail(
            subject=utils.config.EMAIL["outgoing_subject"].format(report.id),
            message=text,
            from_email=utils.config.EMAIL["outgoing_address"],
            recipient_list=[report.email],
            fail_silently=False,
        )
        fragment = f"reply-{msg.id}"
    elif typ == "Note":
        msg = NoteMessage.objects.create(text=text, author=user, report=report)
        fragment = f"note-{msg.id}"
    else:
        assert False, typ

    url = urls.reverse("report_detail", kwargs={"pk": pk})
    return redirect(f"{url}#{fragment}")
