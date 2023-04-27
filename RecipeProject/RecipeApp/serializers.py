from .models import RcpTable
from rest_framework import serializers


class RcpTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RcpTable
        fields = '__all__'