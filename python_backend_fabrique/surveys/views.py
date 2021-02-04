from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as UserModel
from datetime import datetime
from .models import Survey
from .serializers import UserSerializer, SurveySerializer


# -- Sign up -----------------------------------------------------------------
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = UserModel.objects.create_user(
            email = serializer.data['email'],
            username = serializer.data['username'],
            first_name = serializer.data['first_name'],
            last_name = serializer.data['last_name'],
            password = serializer.data['password']
        )
        # user.set_password(serializer.data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


# -- Sign in -----------------------------------------------------------------
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signin(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
    except:
        return Response(
            {'error': 'Please provide correct username and password'},
            status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response(
            {'authenticated': False, 'token': None})


# -- Getting surveys list -----------------------------------------------------
@api_view(['GET']) 
def api_surveys(request):
    if request.method == 'GET':
        current_date = datetime.now().date()
        surveys = Survey.objects.filter(
            start_date__lte=current_date,
            end_date__gt=current_date)
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# -- Getting surveys list -----------------------------------------------------
