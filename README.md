# mappeat_v2
Nueva versión de Mappeat  
Stack:
Python 3.6.0  
Django 1.10.5


###Como activar el entorno virtual:
$ source venv-mappeat/bin/activate

Ahora tendremos de forma automática todas las dependencias listas sin tener que instalarlas con pip3  
Para desactivar el venv solo hay que ejecutar "deactivate"

$ deactivate

Nota: hay que tener en cuenta que mientras tengamos activado el venv (virtual environment) lo que instalemos con pip3 se quedará dentro del venv y no en nuestra version de python local.


###Dependencias:  (Ya incluidas en el venv)
$ pip3 install django   
$ pip3 install djangorestframework  
$ pip3 install django-filter  
$ pip3 install markdown 
$ pip3 install Pillow
$ pip3 install pygments 
$ pip3 install git+https://github.com/RNogales94/django-registration-rest-framework.git
$ pip3 install django-rest-swagger


##Documentacion de la api:  
En la carpeta: mappeat_v2/mappeat/mappeat  
ejecutar:   
$ python3 manage.py runserver  
y entrar en:  
http://127.0.0.1:8000/dev/docs/



