from rest_framework import serializers
from .models import Propaganda

class PropagandaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Propaganda
        fields = '__all__'