import itertools
from typing import Iterable

from django.db import models
from django.utils import timezone
from django.conf import settings

import django_mailbox.models


class Label(models.Model):

    name = models.CharField(max_length=255)
    # FIXME color-field using django-color{ful,field}?
    color = models.CharField(max_length=7)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


class Bin(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='subscribed_bins',
                                         blank=True)
    maintainers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='maintained_bins',
                                         blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    related_bins = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_inbox():
        """Get the inbox bin to be used for new reports."""
        # FIXME Make this configurable
        return Bin.objects.get(name='Inbox')


class Report(models.Model):

    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE,
                            related_name='reports',
                            default=Bin.get_inbox)
    log = models.TextField(blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    def all_messages(self) -> Iterable['Message']:
        return sorted(itertools.chain(
            self.incomingmessage_set.all(),
            self.outgoingmessage_set.all(),
            self.notemessage_set.all()
        ), key=lambda msg: msg.created_at)


class Message(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    NAME = None

    def author(self):
        return '<unknown>'

    def __str__(self):
        return '<{} from {} at {}>'.format(self.NAME, self.author(),
                                           self.created_at.ctime())

    class Meta:

        abstract = True


class IncomingMessage(Message):

    mail = models.ForeignKey(django_mailbox.models.Message,
                             on_delete=models.CASCADE)
    NAME = 'Message'

    def author_str(self):
        return self.mail.from_address[0]

    def contents(self):
        return self.mail.text


class NoteMessage(Message):

    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    NAME = 'Note'

    def author_str(self):
        if self.author is None:
            return '<unknown>'
        else:
            return self.author.get_username()

    def contents(self):
        return self.text


class OutgoingMessage(Message):

    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    NAME = 'Reply'

    def author_str(self):
        if self.author is None:
            return '<unknown>'
        else:
            return self.author.get_username()

    def contents(self):
        return self.text
