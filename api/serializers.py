from rest_framework import serializers
from api.models import CurrentAffair, HeaderImage


class CurrentAffairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAffair
        fields = '__all__'
        

class HeaderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderImage
        fields = '__all__'
