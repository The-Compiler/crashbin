from django import urls
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from crashbin_app.models import Bin, Report


@login_required
def home(request: HttpRequest) -> HttpResponse:
    user = request.user  # type: ignore
    data = {
        'bins': Bin.objects.order_by('created_at'),
        'reports': Report.objects,
        'maintained_bins': Bin.objects.filter(maintainers=user),
        'subscribed_bins': Bin.objects.filter(subscribers=user),
    }
    return render(request, 'crashbin_app/home.html', data)


@login_required
def search_dispatch(request: HttpRequest) -> HttpResponse:
    scope: str = request.GET['scope']
    query: str = request.GET['q']
    if scope == 'Reports':
        url: str = urls.reverse('report_list')
        return redirect('{}?q={}'.format(url, query))
    if scope == 'Bins':
        url: str = urls.reverse('bin_list')
        return redirect('{}?q={}'.format(url, query))
    if scope == 'Labels':
        url: str = urls.reverse('label_list')
        return redirect('{}?q={}'.format(url, query))
    return HttpResponseBadRequest("Invalid scope {}".format(scope))
