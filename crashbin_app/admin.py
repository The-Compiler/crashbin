from django.contrib import admin
from . import models

admin.site.register(models.Label)
admin.site.register(models.Bin)
admin.site.register(models.Report)

# Register your models here.
