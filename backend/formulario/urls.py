from django.urls import path
from django.conf.urls.static import static
#from . import views
from .views import cad_face
from .views import login
from .views import lista_cad
from .views import lista_ace
from .views import config
from .views import sobre
from .views import senha
from .views import alterar

urlpatterns = [
    path(r'', login, name = 'formulario_login'),
    path('Cadastrar', cad_face, name = 'formulario_cad_face'),
    path('UsuáriosCadastrados', lista_cad, name = 'formulario_lista_cad'),
    path('Acessos', lista_ace, name = 'formulario_lista_ace'),
    path('Configuração', config, name = 'formulario_config'),
    path('Sobre', sobre, name = 'formulario_sobre'),
    path('Senha', senha, name = 'formulario_senha'),
    path('Alterar<idp>', alterar, name = 'formulario_alterar'),
]


    