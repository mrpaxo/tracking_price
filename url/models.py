from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from tracking_price.utils import unique_slugify

# Create your models here.

TIEMPO = (('1MIN','1 Minutos'),
            ('5MIN','5 Minutos'),
            ('1HR','1 Hora'))

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class SlugableBehaviour(models.Model):
    '''crear slugs unicos'''
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, **kwargs):
        slug_str = "{}".format(self.nombre)
        unique_slugify(self, slug_str)
        super(SlugableBehaviour, self).save(**kwargs)

    class Meta:
        abstract = True



class ConfUrl(SlugableBehaviour, models.Model):
    nombre = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True, null=True)
    json_value = JSONField( default={}, blank=True)

    def __str__(self):
        return self.slug

        
class Url(BaseModel):
    url = models.URLField(max_length=500)
    user = models.ForeignKey(User , blank = True , null = True , on_delete=models.CASCADE)
    duracion = models.CharField(choices =TIEMPO, default ='5MIN' , max_length = 10)
    conf_url = models.ForeignKey(ConfUrl,blank = True , null = True,on_delete=models.CASCADE)#asi sabremos si es de amazon , mercadolibre etc...
    estado = models.BooleanField(default= True)
    
    def __str__(self):
        return '%s  %s' % (self.url,self.user.username)

class HistorialPrecio(BaseModel):
    precio = models.DecimalField(max_digits = 7 ,decimal_places = 2)
    
    def __str__(self):
        return '%s' % (self.precio)

class Articulo(BaseModel):
    url = models.ForeignKey(Url,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=500)
    hist_precio = models.ManyToManyField(HistorialPrecio)

    def __str__(self):
        return '%s  %s' % (self.url,self.nombre)

