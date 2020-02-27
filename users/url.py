from django.urls import path , include
from rest_framework import routers
from .views import UserViewSet ,signin ,user_info, logout

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns =[
    
  
]
urlpatterns += [
    path('signin', signin),
    path('user_info', user_info),
    path('logout', logout),
    path('', include(router.urls)),

    
]