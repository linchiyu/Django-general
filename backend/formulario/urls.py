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
from .views import logout

urlpatterns = [
    path(r'', login, name = 'formulario_login'),
    path('cadastrar', cad_face, name = 'formulario_cad_face'),
    path('usuarioscadastrados', lista_cad, name = 'formulario_lista_cad'),
    path('acessos', lista_ace, name = 'formulario_lista_ace'),
    path('configuracao', config, name = 'formulario_config'),
    path('sobre', sobre, name = 'formulario_sobre'),
    path('senha', senha, name = 'formulario_senha'),
    path('logout', logout, name = 'formulario_logout'),
    path('alterar/<int:idp>', alterar, name = 'formulario_alterar'),
]
