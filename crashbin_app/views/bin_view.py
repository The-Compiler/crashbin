from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from crashbin_app.forms import InboxBinForm, BinForm
from crashbin_app.models import Bin
from crashbin_app.views.misc_view import back_redirect_ok


@login_required
def bin_list(request: HttpRequest) -> HttpResponse:
    bins = Bin.objects.order_by('created_at')
    if 'q' in request.GET:
        query = request.GET['q']
        bins = bins.filter(name__icontains=query)
    else:
        query = None

    return render(request,
                  'crashbin_app/bins.html',
                  {'bins': bins, 'query': query})


@login_required
def bin_detail(request: HttpRequest, pk: int) -> HttpResponse:
    bin_obj = get_object_or_404(Bin, pk=pk)
    return render(request, 'crashbin_app/bin_detail.html',
                  {'bin': bin_obj})


@login_required
def bin_new_edit(request: HttpRequest, pk: int = None) -> HttpResponse:
    bin_obj = None if pk is None else get_object_or_404(Bin, pk=pk)
    is_inbox = bin_obj == Bin.get_inbox()
    form_cls = InboxBinForm if is_inbox else BinForm
    form = form_cls(request.POST or None, instance=bin_obj)

    if request.method == 'POST' and form.is_valid():
        new_bin = form.save()
        if back_redirect_ok(request):
            return redirect(request.GET['back'])
        return redirect('bin_detail', pk=new_bin.pk)

    if pk is None:
        data = {
            'title': 'New bin',
            'form': form,
        }
    else:
        data = {
            'title': 'Edit bin',
            'form': form,
            'delete_button': '' if is_inbox else 'bin',
            'pk': pk,
            'bin': bin_obj,
        }

    return render(request, 'crashbin_app/form.html', data)


@login_required
@require_POST
def bin_subscribe(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user  # type: ignore
    bin_obj: Bin = get_object_or_404(Bin, pk=pk)
    if user in bin_obj.subscribers.all():
        bin_obj.subscribers.remove(user)
    else:
        bin_obj.subscribers.add(user)
    return HttpResponse()
