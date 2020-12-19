from rest_framework import serializers
from api.models import CurrentAffair, HeaderImage, \
    RollOfHonor, CustomerQuery, VideoContent


class CurrentAffairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAffair
        fields = '__all__'
        

class HeaderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderImage
        fields = '__all__'


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = '__all__'


class RollOfHonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RollOfHonor
        fields = '__all__'

class CustomerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerQuery
        fields = '__all__'