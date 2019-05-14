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
    if request.method == 'POST':
        user = request.user  # type: ignore
        bin: Bin = Bin.objects.get(id=pk)
        if user in bin.subscribers.all():
            bin.subscribers.remove(user)
        else:
            bin.subscribers.add(user)
        return Response(status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_400_BAD_REQUEST)