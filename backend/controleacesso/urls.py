from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

baseurl = 'api'

urlpatterns = [
    path(baseurl+'/pessoa/new', views.PessoaCreate.as_view(), name='cpessoa'),
    path(baseurl+'/pessoa/list', views.PessoaList.as_view(), name='lpessoa'),
    path(baseurl+'/pessoa/update/<int:pk>', views.PessoaUpdate.as_view(), name='upessoa'),

    path(baseurl+'/acesso/new', views.AcessoCreate.as_view(), name='cacesso'),
    path(baseurl+'/acesso/list', views.AcessoList.as_view(), name='lacesso'),
]