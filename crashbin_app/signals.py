import logging

from django.dispatch import Signal, receiver
import django_mailbox.signals

from crashbin_app import models


new_report = Signal(providing_args=['report', 'bin'])


@receiver(django_mailbox.signals.message_received)
def process_incoming_mail(message, **kwargs):  # pylint: disable=unused-argument
    try:
        report = models.Report.for_mail_subject(message.subject)
    except models.InvalidMailError as ex:
        logging.error(str(ex))
        return
    models.IncomingMessage.objects.create(mail=message, report=report)
