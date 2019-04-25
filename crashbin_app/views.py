from django.shortcuts import render, get_object_or_404, redirect

from .models import Report, Bin
from .forms import BinForm


def home(request):
    bins = Bin.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/home.html',
                  {'bins': bins})


def report_list(request):
    reports = Report.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/reports.html',
                  {'reports': reports})


def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'crashbin_app/report_detail.html',
                  {'report': report})


def bin_list(request):
    bins = Bin.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/bins.html',
                  {'bins': bins})


def bin_detail(request, pk):
    bin = get_object_or_404(Bin, pk=pk)
    return render(request, 'crashbin_app/bin_detail.html',
                  {'bin': bin})


def bin_new(request):
    if request.method == 'POST':
        form = BinForm(request.POST)
        if form.is_valid():
            bin = form.save()
            return redirect('bin_detail', pk=bin.pk)
    else:
        form = BinForm()
    return render(request, 'crashbin_app/bin_edit.html',
                  {'form': form})
