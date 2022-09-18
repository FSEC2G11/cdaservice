from rest_framework import serializers
from .models import AnalysisRun


class AnalysisRunSerializer(serializers.ModelSerializer):
    #time = serializers.DateTimeField(format="%Y%m%d%H%M%S%f")

    class Meta:
        model = AnalysisRun
        fields = "__all__"
