from django.shortcuts import render, get_object_or_404, redirect

from .models import Report, Bin
from .forms import BinForm


def home(request):
    num_reports = Report.objects.count()
    num_bins = Bin.objects.count()
    return render(request,
                  'crashbin_app/home.html',
                  {'num_reports': num_reports,
                   'num_bins': num_bins,
                   'title': 'Home'})


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


def bin_new(request):
    if request.method == 'POST':
        form = BinForm(request.POST)
        if form.is_valid():
            bin = form.save()
            return redirect('bin_detail', pk=bin.pk)
    else:
        form = BinForm()
    return render(request, 'crashbin_app/bin_edit.html',
                  {'title': 'New bin', 'form': form})
