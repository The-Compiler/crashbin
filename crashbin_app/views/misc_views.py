import urllib.parse

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
    query: str = urllib.parse.urlencode({'q': request.GET['q']})
    scope_to_view = {
        'Reports': 'report_list',
        'Bins': 'bin_list',
        'Labels': 'label_list',
    }
    if scope not in scope_to_view:
        return HttpResponseBadRequest("Invalid scope {}".format(scope))

    url: str = urls.reverse(scope_to_view[scope])
    return redirect('{}?{}'.format(url, query))


