from django.urls import path, re_path
from . import views


urlpatterns = [
    path('video_feed/<slug:mem_name>/', 
    	lambda request, mem_name: views.videoStream(mem_name), name='video_feed'),
    #path('cftv/', lambda slug: views.videoStream(slug)),
    path('api/server', views.ServerList.as_view(), name='api-list-server'),
    path('api/camera', views.CameraList.as_view(), name='api-list-camera'),
]