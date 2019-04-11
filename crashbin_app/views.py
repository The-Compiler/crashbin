from django.shortcuts import render, get_object_or_404

from .models import Report, Bin


def home(request):
    reports = Report.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/home.html',
                  {'reports': reports, 'title': 'Home'})


def report_list(request):
    reports = Report.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/reports.html',
                  {'reports': reports, 'title': 'Reports'})


def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'crashbin_app/report_detail.html',
                  {'report': report, 'title': 'Report: ' + report.title})


def bin_list(request):
    bins = Bin.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/bins.html',
                  {'bins': bins, 'title': 'Bins'})


def bin_detail(request, pk):
    bin = get_object_or_404(Bin, pk=pk)
    return render(request, 'crashbin_app/bin_detail.html',
                  {'bin': bin, 'title': 'Bin: ' + bin.name})
