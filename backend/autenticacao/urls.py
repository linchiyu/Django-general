from django.urls import path, re_path
from django.conf.urls import url, include
#from . import views
from .views import FacebookLogin
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    #path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    #re_path('rest-auth/registration/account-confirm-email/(?P<key>.+)/', ConfirmEmailView.as_view(), name='account_confirm_email')
]