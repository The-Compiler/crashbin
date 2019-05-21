import typing
from typing import Sequence

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import viewsets, mixins, permissions, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from crashbin_app.api.serializers import ReportSerializer, ReportNewSerializer, BinSerializer
from crashbin_app.models import Report, Bin, Label


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportNew(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReportNewSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BinViewSet(viewsets.ModelViewSet):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer


@api_view(['POST'])
def bin_subscribe(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user  # type: ignore
    bin_obj: Bin = Bin.objects.get(id=pk)
    if user in bin_obj.subscribers.all():
        bin_obj.subscribers.remove(user)
    else:
        bin_obj.subscribers.add(user)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def set_settings(request: HttpRequest, pk: int, scope: str) -> HttpResponse:
    element: typing.Union[Report, Bin]
    redirect_path: str
    query_list: Sequence = request.POST.getlist(key=scope)

    if request.path.startswith('/api/bins/'):
        element = Bin.objects.get(id=pk)
        redirect_path = 'bin_detail'
    elif request.path.startswith('/api/reports/'):
        element = Report.objects.get(id=pk)
        redirect_path = 'report_detail'
    else:
        return HttpResponseBadRequest("Invalid request")

    if scope == 'maintainer':
        assert isinstance(element, Bin)
        element.maintainers.clear()
        for maintainer in query_list:
            element.maintainers.add(User.objects.get(id=maintainer))
    elif scope == 'label':
        element.labels.clear()
        for label in query_list:
            element.labels.add(Label.objects.get(id=label))
    elif scope == 'related':
        assert isinstance(element, Bin)
        element.related_bins.clear()
        for related_bin in query_list:
            element.related_bins.add(Bin.objects.get(id=related_bin))
    elif scope == 'assigned':
        assert isinstance(element, Report)
        element.bin = Bin.objects.get(id=query_list[0])
        element.save()
    else:
        return HttpResponseBadRequest("Invalid request")
    return redirect(redirect_path, pk=pk)
