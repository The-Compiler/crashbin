from django.db import models
from django.utils import timezone
from django.conf import settings


class Label(models.Model):

    name = models.CharField(max_length=255)
    # FIXME color-field using django-color{ful,field}?
    color = models.CharField(max_length=7)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
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

    def __str__(self):
        return self.name


class Report(models.Model):

    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE,
                            related_name='reports')
    log = models.TextField(blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
