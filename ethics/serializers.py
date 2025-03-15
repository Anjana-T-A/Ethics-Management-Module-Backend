# serializers.py

from rest_framework import serializers
from .models import EthicsForm

class EthicsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthicsForm
        fields = '__all__'
