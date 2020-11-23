from rest_framework import serializers
from api.models import CurrentAffair


class CurrentAffairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAffair
        fields = '__all__'
        