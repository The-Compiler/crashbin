import typing
import attr

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from crashbin_app.models import Report, Bin, Label


@login_required
@require_http_methods(["GET", "POST"])
def settings(request: HttpRequest, pk: int, setting: str) -> HttpResponse:
    target: typing.Union[Report, Bin]
    if request.path.startswith("/bin/"):
        target = get_object_or_404(Bin, pk=pk)
    elif request.path.startswith("/report/"):
        target = get_object_or_404(Report, pk=pk)
    else:
        raise AssertionError("Invalid path {}".format(request.path))

    if request.method == "GET":
        return _get_settings(request, target, setting)
    if request.method == "POST":
        return _set_settings(request, target, setting)
    raise AssertionError("Invalid method {}".format(request.method))


@attr.s
class _ButtonInfo:
    text: str = attr.ib()
    view: str = attr.ib()


def _get_settings(
    request: HttpRequest, target: typing.Union[Bin, Report], setting: str
) -> HttpResponse:
    Element = typing.Union[User, Label, Bin]
    all_elements: QuerySet
    selected_elements: typing.Iterable[Element]
    title: str
    new_button: typing.Optional[_ButtonInfo] = None

    if setting == "maintainer":
        assert isinstance(target, Bin)
        all_elements = User.objects.order_by("id")
        selected_elements = target.maintainers.all()
        title = "Maintainers for {}".format(target)
    elif setting == "label":
        all_elements = Label.objects.order_by("created_at")
        new_button = _ButtonInfo("New label", "label_new_edit")
        selected_elements = target.labels.all()
        title = "Labels for {}".format(target)
    elif setting == "related":
        assert isinstance(target, Bin)
        new_button = _ButtonInfo("New bin", "bin_new_edit")
        all_elements = Bin.objects.exclude(id=target.id)
        selected_elements = target.related_bins.all()
        title = "Related to {}".format(target)
    elif setting == "bin":
        assert isinstance(target, Report)
        new_button = _ButtonInfo("New bin", "bin_new_edit")
        all_elements = Bin.objects.order_by("created_at")
        selected_elements = [target.bin]
        title = "Bin for {}".format(target)
    else:
        return HttpResponseBadRequest("Invalid setting request")

    data = {
        "pk": target.id,
        "setting": setting,
        "all_elements": all_elements,
        "selected_elements": selected_elements,
        "title": title,
        "new_button": new_button,
    }
    return render(request, "crashbin_app/set_settings.html", data)


def _set_settings(
    request: HttpRequest, target: typing.Union[Bin, Report], setting: str
) -> HttpResponse:
    redirect_view: str
    query_list: typing.Sequence = request.POST.getlist(key=setting)

    if setting == "maintainer":
        assert isinstance(target, Bin)
        target.maintainers.clear()
        for maintainer in query_list:
            target.maintainers.add(User.objects.get(id=maintainer))
    elif setting == "label":
        target.labels.clear()
        for label in query_list:
            target.labels.add(Label.objects.get(id=label))
    elif setting == "related":
        assert isinstance(target, Bin)
        target.related_bins.clear()
        for related_bin in query_list:
            target.related_bins.add(Bin.objects.get(id=related_bin))
    elif setting == "bin":
        assert isinstance(target, Report)
        user = request.user  # type: ignore
        bin_obj = Bin.objects.get(id=query_list[0])
        target.assign_to_bin(bin_obj, user=user)
    else:
        return HttpResponseBadRequest("Invalid setting request")

    redirect_view = "bin_detail" if isinstance(target, Bin) else "report_detail"
    return redirect(redirect_view, pk=target.id)
