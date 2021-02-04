from django.urls import path
# from rest_framework.authtoken import views
from .views import api_signup, api_signin, api_surveys


urlpatterns = [
    path('signup/', api_signup),
    path('signin/', api_signin),
    path('surveys/', api_surveys),
]
