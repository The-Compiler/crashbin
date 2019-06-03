from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from crashbin_app.models import Bin, Report
from crashbin_app.views.bin_views import bin_list
from crashbin_app.views.report_views import report_list


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
    if scope == 'Reports':
        return report_list(request)
    if scope == 'Bins':
        return bin_list(request)
    return HttpResponseBadRequest("Invalid scope {}".format(scope))
