import typing

from rest_framework import viewsets, mixins, permissions, generics
from rest_framework.request import Request
from rest_framework.response import Response

from crashbin_app.api.serializers import (
    ReportSerializer,
    ReportNewSerializer,
    BinSerializer,
    LabelSerializer,
)
from crashbin_app.models import Report, Bin, Label


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportNew(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReportNewSerializer

    def post(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return self.create(request, *args, **kwargs)


class BinViewSet(viewsets.ModelViewSet):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
