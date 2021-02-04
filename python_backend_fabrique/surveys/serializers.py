from rest_framework import serializers
from .models import User, Survey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'username',
            'first_name',
            'last_name',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = (
            'pk',
            'title',
            'description',
            'start_date',
            'end_date')
