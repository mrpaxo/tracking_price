from bs4 import BeautifulSoup
from django.core.mail import send_mail
import requests , re
from django.conf import settings

def get_soup(url,gral_conf):
    headers ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    pagina = requests.get(url, headers = headers)
    soup = BeautifulSoup(pagina.content,'html.parser')   
    precio = get_price(soup,gral_conf.get('conf_precio'))
    titulo = get_title(soup,gral_conf.get('conf_titulo'))
    soup = {'valido':False, 'precio': 0 , 'titulo':''}

    if precio.get('valido') == True & titulo.get('valido') == True:
        soup['valido'] = True
        soup['precio'] = precio.get('precio')
        soup['titulo'] = titulo.get('titulo')
    return soup

def get_price(soup,conf_precio):
    response = {'valido':False,'precio':0}
    for price in conf_precio:
        if price.get('tipo') == 'id':
            precio = soup.find(id = price.get('precio'))
        elif price.get('tipo') == 'class':
            precio = soup.find(price.get('etiqueta'), {"class": price.get('precio')})
        else:
            precio = None

        if precio != None:
            precio = precio.get_text().strip() 
            precio_convertido = re.sub('\,', '', precio)
            precio_convertido = float(re.sub('\$', '', precio_convertido))
            response['valido'] = True
            response['precio'] = precio_convertido
            return response
        else:
            print('no encontre price')
    return response

def get_title (soup,conf_titulo):
    response = {'valido':False,'titulo':0}
    for titulo in conf_titulo:
        if titulo.get('tipo') == 'id':
            titulo = soup.find(id = titulo.get('titulo'))
        elif titulo.get('tipo') == 'class':
            titulo = soup.find(titulo.get('etiqueta'), {"class": titulo.get('titulo')})
        else : 
            titulo = None

        if titulo != None:
            response['valido'] = True
            response['titulo'] = titulo.get_text().strip() 
            return response
        else:
            print('no encontre titulo')
    return response
    
def send_email(subject, mensaje ,email):
    try:

        send_mail(
        subject,
        mensaje,
        settings.EMAIL_HOST_USER,
        email,
        fail_silently=False,
    )
        print('enviado exitosamente')
    except Exception as e:
        print(e)

def cantidades_iguales(num1 , num2):
    print(num1,num2,'-----------------')
    if num1 != num2:
        return True
    else:
        return False