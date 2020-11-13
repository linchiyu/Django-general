from django.urls import path, re_path
from . import views

baseurl = 'api'

urlpatterns = [
    path(baseurl+'/propaganda', views.PropagandaApi.as_view(), name='propagandaapi'),
]