from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, mixins, permissions, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from crashbin_app.api.serializers import ReportSerializer, ReportNewSerializer, BinSerializer
from crashbin_app.models import Report, Bin


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
