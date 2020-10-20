from django.urls import path, re_path
from . import views


urlpatterns = [
    path('cftv/<slug:mem_name>', lambda x, mem_name: views.videoStream(mem_name)),
    #path('cftv/', lambda slug: views.videoStream(slug)),
    path('api/server', views.ServerList.as_view(), name='api-list-server'),
    path('api/camera', views.CameraList.as_view(), name='api-list-camera'),
]