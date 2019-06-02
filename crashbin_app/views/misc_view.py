from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.http import is_safe_url

from crashbin_app.models import Bin, Report
from crashbin_app.templatetags.components import report_list, bin_list


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


def back_redirect_ok(request: HttpRequest):
    if 'back' not in request.GET:
        return False
    return is_safe_url(request.GET['back'], allowed_hosts=None)
