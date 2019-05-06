from crashbin_app.api.serializers import ReportSerializer

from rest_framework import mixins, permissions, generics


class ReportNew(mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)