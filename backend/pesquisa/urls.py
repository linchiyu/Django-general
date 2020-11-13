from django.urls import path, re_path
from . import views

baseurl = 'api'

urlpatterns = [
    path(baseurl+'/satisfacao', views.SatisfacaoApi.as_view(), name='satisfacaoapi'),
]