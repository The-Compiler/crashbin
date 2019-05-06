from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse

from .models import Report, Bin
from .forms import BinForm


def home(request: HttpRequest) -> HttpResponse:
    bins = Bin.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/home.html',
                  {'bins': bins})


def report_list(request: HttpRequest) -> HttpResponse:
    reports = Report.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/reports.html',
                  {'reports': reports})


def report_detail(request: HttpRequest, pk: int) -> HttpResponse:
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'crashbin_app/report_detail.html',
                  {'report': report})


def bin_list(request: HttpRequest) -> HttpResponse:
    bins = Bin.objects.order_by('created_at')
    return render(request,
                  'crashbin_app/bins.html',
                  {'bins': bins})


def bin_detail(request: HttpRequest, pk: int) -> HttpResponse:
    bin_obj = get_object_or_404(Bin, pk=pk)
    return render(request, 'crashbin_app/bin_detail.html',
                  {'bin': bin_obj})


def bin_new(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BinForm(request.POST)
        if form.is_valid():
            bin_obj = form.save()
            return redirect('bin_detail', pk=bin_obj.pk)
    else:
        form = BinForm()
    return render(request, 'crashbin_app/bin_edit.html',
                  {'form': form})
