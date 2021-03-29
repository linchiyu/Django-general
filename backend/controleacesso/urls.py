from django.urls import path, re_path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

baseurl = 'api'

urlpatterns = [
    path(baseurl+'/pessoa/create', views.PessoaApiCreate.as_view(), name='capipessoa'),
    path(baseurl+'/pessoa/createb64', views.PessoaApiCreateB64.as_view(), name='capipessoab64'),
    path(baseurl+'/pessoa/list', views.PessoaList.as_view(), name='lpessoa'),
    path(baseurl+'/pessoa/facelist', views.PessoaFace.as_view(), name='flpessoa'),
    path(baseurl+'/pessoa/update/<int:pk>', views.PessoaUpdate.as_view(), name='upessoa'),
    path(baseurl+'/pessoa/updateb64/<int:pk>', views.PessoaUpdateB64.as_view(), name='upessoab64'),
    path(baseurl+'/pessoa/<int:pk>', views.PessoaRetrieve.as_view(), name='rpessoa'),

    path(baseurl+'/pessoa/process', views.PessoaProcessList.as_view(), name='procpessoa'),
    path(baseurl+'/pessoa/process/<int:pk>', views.PessoaProcessUpdate.as_view(), name='upprocpessoa'),

    path(baseurl+'/acesso/new', views.AcessoCreate.as_view(), name='cacesso'),
    path(baseurl+'/acesso/list', views.AcessoList.as_view(), name='lacesso'),
    #re_path(r'^api/acesso/list/(?P<idpessoa>\w+)/$', views.AcessoList.as_view(), name='lacesso'),
]