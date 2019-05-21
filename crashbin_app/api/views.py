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
