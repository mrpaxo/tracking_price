
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import  serializers , status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Url , Articulo , ConfUrl ,HistorialPrecio


from .utils import get_soup, get_price

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        exclude = ['conf_url']

    @transaction.atomic()
    def create(self, validated_data):      
        url = validated_data['url']  
        dominio = url.split('.')              
        conf_dominio = None
        validated_data['user'] = User.objects.get(pk = self.context.get('request').user.pk)
        try:           
            conf_dominio = ConfUrl.objects.get(nombre = dominio[1])            
        except :            
            raise serializers.ValidationError("Las Url del siguiente sitio "+dominio[1].upper()+" no son soportados")

        if conf_dominio:
            soup = get_soup(url,conf_dominio.json_value)                                    
            if soup.get('valido') == True:                
                url = Url.objects.create(**validated_data)
                url.conf_url = conf_dominio
                url.save()
                
                a = Articulo.objects.create(url = url,nombre= soup.get("titulo"))
                a.hist_precio.create(precio = soup.get("precio")) 
            else:
                raise serializers.ValidationError("Ocurrio un error")
        return url

class HistorialPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPrecio
        fields = serializers.ALL_FIELDS

class ArticuloSerializer(serializers.ModelSerializer):
    url = UrlSerializer()
    hist_precio = HistorialPrecioSerializer(many=True)
    class Meta:
        model = Articulo
        fields = serializers.ALL_FIELDS

