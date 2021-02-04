from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views


urlpatterns = [
    path('signup/', views.api_signup),
    path('signin/', auth_views.obtain_auth_token),
    path('surveys/', views.api_surveys_list),
    path('surveys/<int:id>/', views.api_surveys_list),
    path('surveys/<int:id>/anonymously/', views.api_survey_anonymously),
    path('answers/', views.api_answers),
]
