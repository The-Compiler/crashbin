from crashbin_app.api.serializers import ReportSerializer

from rest_framework import mixins, permissions, generics
from django.views.decorators.csrf import csrf_exempt


class ReportNew(mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = ReportSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
