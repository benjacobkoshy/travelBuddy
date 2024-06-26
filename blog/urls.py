"""
URL configuration for travell_buddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views 


urlpatterns = [
    path('create_blog/<int:user_id>/', views.create_blog, name='create_blog'),
    path('like/<int:pk>',views.LikeView,name="like_post"),
    path('comment/<int:blog_id>/',views.Comments,name="comment"),
    path('add-to-bookmark/<int:blog_id>/', views.add_to_bookmark, name='bookmark'),
    path('delete/<int:blog_id>/',views.deleteBlog,name="delete-blog"),
    

]

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
