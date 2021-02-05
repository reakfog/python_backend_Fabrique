from rest_framework import serializers
from .models import User, Survey, Question, Answer


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'pk',
            'text',
            'answer_type',
            'answer_choices',
            'survey',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'text',
            'anonimously',
            'question',
            'author',)
