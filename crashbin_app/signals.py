import logging
import typing

from django.dispatch import Signal, receiver
import django.db.models.signals
from django_mailbox.models import Message
import django_mailbox.signals

from crashbin_app import models

# Receivers need to have a **kwargs argument.
# pylint: disable=unused-argument

new_report = Signal(providing_args=["report"])
bin_assigned = Signal(providing_args=["report", "old_bin", "new_bin", "user"])


@receiver(django_mailbox.signals.message_received)
def process_incoming_mail(message: Message, **kwargs: typing.Any) -> None:
    try:
        report = models.Report.for_mail_subject(message.subject)
    except models.InvalidMailError as ex:
        logging.error(str(ex))
        return
    models.IncomingMessage.objects.create(mail=message, report=report)


@receiver(django.db.models.signals.post_save, sender=models.Report)
def report_saved(created: bool, instance: models.Report, **kwargs: typing.Any) -> None:
    if created:
        new_report.send(sender=None, report=instance)
