from django.db import models
from django.utils import timezone
from django.conf import settings


class Label(models.Model):

    name = models.CharField(max_length=255)
    # FIXME color-field using django-color{ful,field}?
    color = models.CharField(max_length=7)
    description = models.TextField()


class Bin(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='subscribed_bins')
    maintainers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='maintained_bins')
    labels = models.ManyToManyField(Label)
    related_bins = models.ManyToManyField('self')


class Report(models.Model):

    email = models.EmailField()
    created_date = models.DateTimeField(default=timezone.now)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)
