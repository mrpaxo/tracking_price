"""tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from users.views import signin, user_info, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('url/',include('url.url')),
    path('users/',include('users.url')),
    path('api-auth/',ObtainAuthToken.as_view()),
    #path('users/signin', signin),
    #path('users/user_info', user_info),
    #path('users/logout', logout),
    #path('api-auth/',include('rest_framework.urls'))
]
