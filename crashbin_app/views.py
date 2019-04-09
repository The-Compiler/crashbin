from django.shortcuts import render

from .models import Report


def home(request):
    reports = Report.objects.order_by('created_at')
    return render(request, 'crashbin_app/home.html', {'reports': reports})
