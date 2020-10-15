from django.urls import path, re_path
from . import views


urlpatterns = [
    path('cctv/', lambda r: views.videoStream())
]