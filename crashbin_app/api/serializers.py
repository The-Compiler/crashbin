from rest_framework import serializers
from crashbin_app.models import Report, Bin, Label


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('bin', 'labels')


class ReportNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('email', 'log', 'title')


class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ('name', 'description', 'subscribers', 'maintainers', 'labels', 'related_bins',
                  'is_archived')


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('name', 'description', 'color')
