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
from django.urls import path,include
from django.conf.urls.static import static
from user import views


urlpatterns = [
    path('account/',views.show_account,name='account'),
    path('otpVerification/',views.otp_verification,name='otp_verification'),
    path('logout/',views.Logout,name='logout'),
    path('more-details/<int:user_id>/', views.more_details, name='more-details'),
    path('user-account/<int:blog_id>/',views.userAccount,name="user-account"),
    path('owner-account/<int:user_id>/',views.ownerAccount,name="owner-account"),
    path('account-edit/<int:user_id>/',views.accountEdit,name="account-edit"),
    path('deletAccount/<int:user_id>/',views.deleteAccount,name='delete-account'),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)