from crashbin_app.api.serializers import ReportSerializer
# from crashbin_app.models import Report

from rest_framework import mixins, permissions, generics
from django.views.decorators.csrf import csrf_exempt


class ReportNew(mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)

    # queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
