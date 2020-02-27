from django.urls import path , include
from rest_framework import routers
from .views import UrlViewSet ,ArticuloViewSet

router = routers.DefaultRouter()

router.register(r'url-app', UrlViewSet,'url-app')
router.register(r'articulo-app', ArticuloViewSet,'articulo-app')

urlpatterns =[
    
  
]
urlpatterns += [
    path('', include(router.urls)),
]