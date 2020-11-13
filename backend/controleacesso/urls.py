from django.urls import path, re_path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

baseurl = 'api'

urlpatterns = [
    path(baseurl+'/pessoa', views.PessoaApi.as_view(), name='pessoaapi'),

    path(baseurl+'/acesso', views.AcessoApi.as_view(), name='acessoapi'),

    path(baseurl+'/totem', views.TotemApi.as_view(), name='totemapi'),
]