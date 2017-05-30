# mappeat_v2
Nueva versión de Mappeat  
Stack:
Python 3.6.0  
Django 1.10.5

Paquetes necesarios:  


pip3 install django   
pip3 install djangorestframework  
pip3 install django-filter  
pip3 install markdown 
pip3 install Pillow
pip3 install pygments 
pip3 install git+https://github.com/RNogales94/django-registration-rest-framework.git
pip3 install django-rest-swagger


 

En la carpeta principal (la que tiene el 'manage.py'):
pip3 install -e ./django-registration-rest-framework

##Documentacion de la api:  
En la carpeta: mappeat_v2/mappeat/mappeat  
ejecutar:   
python3 manage.py runserver  
y entrar en:  
http://127.0.0.1:8000/dev/docs/


