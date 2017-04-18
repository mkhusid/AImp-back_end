from requests.status_codes import title
from rest_framework import serializers
from .models import Audio,SUser
from django.contrib.auth.models import User


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('person','title')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SUser
        fields = ('username','email')

