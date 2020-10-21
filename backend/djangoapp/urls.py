"""general URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
#from django_private_chat import urls as django_private_chat_urls

admin.site.site_header = "Articfox Admin"
admin.site.site_title = "Articfox Admin"
admin.site.index_title = "Articfox Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/defender/', include('defender.urls')), # defender admin
    #path('', include('autenticacao.urls')),
    #path('', include('controleacesso.urls')),
    #path('', include('formulario.urls')),
    #path('', include('pagamento.urls')),
	#path('', include('django_private_chat.urls')),
    path('', include('cftv.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)