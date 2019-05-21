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
    bin_obj: Bin
    report_obj: Report
    redirect_path: str
    query_list = request.POST.getlist(key=scope)

    if request.path.__contains__('bins'):
        bin_obj = Bin.objects.get(id=pk)
        redirect_path = 'bin_detail'
    elif request.path.__contains__('reports'):
        report_obj = Report.objects.get(id=pk)
        redirect_path = 'report_detail'
    else:
        return HttpResponseBadRequest("Invalid request")

    if scope == 'maintainer':
        bin_obj.maintainers.clear()
        for maintainer in query_list:
            bin_obj.maintainers.add(User.objects.get(id=maintainer))
    elif scope == 'label':
        if bin_obj is not None:
            bin_obj.labels.clear()
            for label in query_list:
                bin_obj.labels.add(Label.objects.get(id=label))
        elif report_obj is not None:
            report_obj.labels.clear()
            for label in query_list:
                report_obj.labels.add(Label.objects.get(id=label))
        else:
            return HttpResponseBadRequest("Invalid request")
    elif scope == 'related':
        bin_obj.related_bins.clear()
        for related_bin in query_list:
            bin_obj.related_bins.add(Bin.objects.get(id=related_bin))
    elif scope == 'assigned':
        report_obj.bin = Bin.objects.get(id=query_list[0])
    else:
        return HttpResponseBadRequest("Invalid request")
    return redirect(redirect_path, pk=pk)
