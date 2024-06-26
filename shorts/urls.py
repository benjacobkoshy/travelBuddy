from django.contrib import admin
from django.urls import path
from . import views 


urlpatterns = [
    path('shorts/',views.shortVideo,name='short-video'),
    path('createShorts/<int:user_id>',views.createVideo,name='create-video'),
    path('deleteShorts/<int:video_id>/',views.deleteShorts,name="delete-shorts")
]
