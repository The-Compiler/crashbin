from django.shortcuts import render, get_object_or_404

from .models import Report


def home(request):
    reports = Report.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/home.html',
                  {'reports': reports, 'title': 'Home'})


def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'crashbin_app/report_detail.html',
                  {'report': report, 'title': 'Report: ' + report.title})
