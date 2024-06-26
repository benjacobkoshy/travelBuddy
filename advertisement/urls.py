from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views 


urlpatterns = [
    path('createAdvertisement/<int:user_id>/', views.advertisement, name='advertisement'),
    path('deleteAdvertisement/<int:adv_id>/',views.deleteAdvertisement,name="delete-advertisement"),
    # path('displayAdvertisement/',)
]