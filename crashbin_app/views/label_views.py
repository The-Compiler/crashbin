from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from crashbin_app.forms import LabelForm
from crashbin_app.models import Label
from crashbin_app.utils import back_redirect_ok


@login_required
def label_list(request: HttpRequest) -> HttpResponse:
    labels = Label.objects.order_by('created_at')
    if 'q' in request.GET:
        query = request.GET['q']
        labels = labels.filter(name__icontains=query)
    else:
        query = None

    return render(request,
                  'crashbin_app/labels.html',
                  {'labels': labels, 'query': query})


@login_required
def label_new_edit(request: HttpRequest, pk: int = None) -> HttpResponse:
    label_obj = None if pk is None else get_object_or_404(Label, pk=pk)
    form = LabelForm(request.POST or None, instance=label_obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        if back_redirect_ok(request):
            return redirect(request.GET['back'])
        return redirect('label_list')

    if pk is None:
        data = {
            'title': 'New label',
            'form': form,
        }
    else:
        label_obj = get_object_or_404(Label, pk=pk)
        data = {
            'title': 'Edit label',
            'form': form,
            'delete_button': 'label',
            'pk': pk,
        }
    return render(request, 'crashbin_app/form.html', data)
