from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
#from . import views
#from .views import FacebookLogin
#from allauth.account.views import ConfirmEmailView


pre_link = 'auth'

urlpatterns = [
    #path('accounts/', include('allauth.urls')),
    path(pre_link+'/', include('dj_rest_auth.urls')),
    path(pre_link+'/registration/', include('dj_rest_auth.registration.urls')),
    #path(pre_link+'/facebook/', FacebookLogin.as_view(), name='fb_login'),
    #re_path('rest-auth/registration/account-confirm-email/(?P<key>.+)/', ConfirmEmailView.as_view(), name='account_confirm_email')
]