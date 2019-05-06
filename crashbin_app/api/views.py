from crashbin_app.api.serializers import ReportSerializer
from crashbin_app.models import Report

from rest_framework import viewsets


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
