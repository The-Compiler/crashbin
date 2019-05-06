from rest_framework import serializers
from crashbin_app.models import Report


class ReportSerializer(serializers.ModelSerializer):

    class Meta:

        model = Report
        fields = ('email', 'log', 'title')
