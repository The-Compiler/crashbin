import re
import itertools
import typing

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import colorful.fields
import django_mailbox.models

from crashbin_app import utils


class Label(models.Model):

    name = models.CharField(max_length=255, unique=True)
    color = colorful.fields.RGBColorField(colors=utils.config.LABEL_COLORS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Bin(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="subscribed_bins", blank=True
    )
    maintainers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="maintained_bins", blank=True
    )
    labels = models.ManyToManyField(Label, blank=True)
    related_bins = models.ManyToManyField("self", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_inbox() -> "Bin":
        """Get the inbox bin to be used for new reports."""
        return Bin.objects.get(name=utils.config.INBOX_BIN)

    class Meta:
        ordering = ["name"]


class InvalidMailError(Exception):

    pass


class Report(models.Model):

    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    bin = models.ForeignKey(
        Bin, on_delete=models.CASCADE, related_name="reports", default=Bin.get_inbox
    )
    log = models.TextField(blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    def all_messages(self) -> typing.Sequence["Message"]:
        return sorted(
            itertools.chain(
                self.incomingmessage_set.all(),  # type: ignore
                self.outgoingmessage_set.all(),  # type: ignore
                self.notemessage_set.all(),  # type: ignore
            ),
            key=lambda msg: msg.created_at,
        )

    def assign_to_bin(self, new_bin: Bin, *, user: User = None) -> None:
        """Assign this report to a bin."""
        from crashbin_app import signals

        old_bin = self.bin
        self.bin = new_bin
        self.save()
        signals.bin_assigned.send(
            sender=self.__class__,
            report=self,
            old_bin=old_bin,
            new_bin=self.bin,
            user=user,
        )

    @staticmethod
    def for_mail_subject(subject: str) -> "Report":
        pattern = utils.config.EMAIL["incoming_subject"]
        match = re.fullmatch(pattern, subject)
        if match is None:
            raise InvalidMailError(
                f"Got incoming email with unknown subject: {subject}"
            )

        try:
            report_id = int(match.group(1))
        except ValueError:
            raise InvalidMailError(
                f"Could not parse report ID from mail subject: {subject}"
            )

        try:
            return Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            raise InvalidMailError(f"Could not find report for mail: {subject}")

    class Meta:
        ordering = ["title"]


class Message(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    NAME: typing.Optional[str] = None

    def __str__(self) -> str:
        return f"{self.NAME} from {self.author_str()} at {self.created_at.ctime()}"

    def author_str(self) -> str:
        raise NotImplementedError

    def contents(self) -> str:
        raise NotImplementedError

    class Meta:

        abstract = True


class IncomingMessage(Message):

    mail = models.ForeignKey(django_mailbox.models.Message, on_delete=models.CASCADE)
    NAME = "Message"

    def author_str(self) -> str:
        return self.mail.from_address[0]

    def contents(self) -> str:
        return self.mail.text


class NoteMessage(Message):

    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    NAME = "Note"

    def author_str(self) -> str:
        if self.author is None:
            return "<unknown>"
        return self.author.get_username()

    def contents(self) -> str:
        return self.text


class OutgoingMessage(Message):

    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    NAME = "Reply"

    def author_str(self) -> str:
        if self.author is None:
            return "<unknown>"
        return self.author.get_username()

    def contents(self) -> str:
        return self.text
