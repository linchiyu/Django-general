from django.urls import path, re_path
from django.conf.urls import url, include
#from . import views
from .views import FacebookLogin

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
	re_path('rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
]