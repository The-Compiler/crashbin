from django.contrib import admin
from . import models

admin.site.register(models.Label)
admin.site.register(models.Bin)
admin.site.register(models.Report)
admin.site.register(models.IncomingMessage)
admin.site.register(models.NoteMessage)
admin.site.register(models.OutgoingMessage)
