from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User as UserModel
from datetime import datetime
from .models import Question, Survey, Answer
from . import serializers


# -- Sign up -----------------------------------------------------------------
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        user = UserModel.objects.create_user(
            email = serializer.validated_data['email'],
            username = serializer.validated_data['username'],
            first_name = serializer.validated_data['first_name'],
            last_name = serializer.validated_data['last_name'],
            password = serializer.validated_data['password']
        )
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


# -- Getting surveys list -----------------------------------------------------
@api_view(['GET']) 
def api_surveys_list(request):
    if request.method == 'GET':
        current_date = datetime.now().date()
        surveys = Survey.objects.filter(
            start_date__lte=current_date,
            end_date__gt=current_date)
        serializer = serializers.SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# -- Taking a survey and answering questions----------------------------------
# -- Не удалось реализовать проверку соответствия ответов на вопросы и
# -- вариантов ответов.
@api_view(['GET', 'POST']) 
def api_survey(request, id):
    if request.method == 'GET':
        questions = Question.objects.filter(survey=id)
        serializer = serializers.QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = serializers.AnswerSerializer(data=request.data)
        if serializer.is_valid():
            # check if anonimously
            if serializer.validated_data['anonimously'] == True:
                serializer.save(author=None)
            else:
                serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -- Getting user answers -----------------------------------------------------
# -- Не удалось детализировать опросы до ответов пользователя. Смогу составить
# -- SQL запрос, однако через Django ORM способа пока не нашел.
@api_view(['GET'])
def api_answers(request):
    if request.method == 'GET':
        answers = Answer.objects.filter(author=request.user)
        serializer = serializers.AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
