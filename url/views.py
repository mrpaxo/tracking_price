from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.db import transaction
from django.contrib.auth.models import User
from .serializers import  UrlSerializer ,ArticuloSerializer
from .models import Url , Articulo
from .utils import get_soup, get_price , send_email , cantidades_iguales
from celery.schedules import crontab
from celery.task import periodic_task
import re
from rest_framework.permissions import  AllowAny
from users.serializers import UserSerializer 


class UrlViewSet(viewsets.ModelViewSet):

    serializer_class = UrlSerializer
    def get_queryset(self):
        queryset = Url.objects.all().order_by('-created_date')
        if self.request.auth:
            queryset = queryset.filter(user = self.request.user.pk)
        else:
            queryset = None
            
        return queryset

class ArticuloViewSet(viewsets.ModelViewSet):

    serializer_class = ArticuloSerializer
    def get_queryset(self):
        queryset = Articulo.objects.all().order_by('created_date')
        if self.request.auth:
            queryset = queryset.filter(url__user = self.request.user.pk)
        else:
            queryset = None
            
        return queryset

@periodic_task(run_every=crontab(), name="test", ignore_result=True)
def test():
    print('ejecutando 1 min')
    main_ejecuta('1MIN')

@periodic_task(run_every=crontab(minute='*/1'), name="ejecuta_5min", ignore_result=True)
def ejecuta_5min():
    print('ejecutando 5 min')
    main_ejecuta('5MIN')
    
def numero():
    pass


    #precio_convertido = re.sub('(\$[0-9,]+(\.[0-9]{2})?)','', a)
    
    #precio_convertido = re.sub('\,', '', a)
    #precio_convertido = float(re.sub('\$', '', precio_convertido))
    
    #print(precio_convertido)
  

    

@transaction.atomic()
def main_ejecuta(duracion):
    query = Url.objects.filter(estado=True,duracion=duracion)    
    email = list()
    if query:
        for q in query:
            soup = get_soup(q.url,q.conf_url.json_value)
            if soup.get('valido') == True: 
                art = Articulo.objects.get(url=q.pk)
                diferente = cantidades_iguales(soup.get('precio'),float(str(art.hist_precio.all().last())))#precio actual vs ultimo precio registrado
                if diferente:
                    art.hist_precio.create(precio = soup.get('precio')) 
                    print('el precio cambio :O')
                    '''email.append(q.user.email)
                    subject = 'Cambio de precio'
                    mensaje = 'El precio de su articulo ha cambiado ,favor de verificarlo'
                    send_email(subject,mensaje,email)'''
                else:
                    print('el articulo no ha cambiado :/')
    else:
        print('No hay query por ejecutar')
