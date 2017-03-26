"""
NOTA:
Este script debe ejecutarse una unica vez para inicializar la base de datos
La forma correcta de ejecutarlo es mediante: python3 manage.py < meteo/initCiudades.py
"""

import urllib.request
from pprint import pprint
import ssl
import json

from geo.models import *
from meteo.models import *
from meteo import AEMET


ssl._create_default_https_context = ssl._create_unverified_context

estaciones = Estacion.objects.all()
estacion = Estacion.objects.all()[0]
#for estacion in estaciones:
#Indent:
fechaini = "2017-01-01T00%3A00%3A00UTC"
fechafin = "2017-01-10T00%3A00%3A00UTC"
url  = urllib.request.urlopen("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/"+fechaini+"/fechafin/"+fechafin+"/estacion/"+estacion.indicativo+"/?api_key="+AEMET.API_KEY) 

data = json.loads(url.read())
meteo = urllib.request.urlopen(data['datos'])
meteo =  str(meteo.read(), 'latin-1')  #Pasamos a unicode para que no haya problemas con las Ñ's etc
meteoJSON = json.loads(meteo)

#print("CHACHIS: "+str(len(meteoJSON)))

num_dias = len(meteoJSON)
for registro_diario in range(0, num_dias):
    print(float((meteoJSON[registro_diario]['tmed'].replace(',', '.'))))


"""
estaciones = [ [meteoJSON[item]['indicativo'], meteoJSON[item]['provincia'], meteoJSON[item]['nombre'], meteoJSON[item]['altitud']] for item in range(0, len(meteoJSON))]
#print(*ciudad_provincia)
"""


"""
for i in estaciones:
    #print(i[0], i[1], i[2], i[3])
    estacion = Estacion(indicativo=str(i[0]), nombre=i[1], provincia=Provincia.objects.get(nombre=i[1]), ciudad=Ciudad.objects.get(nombre=i[2]), altitud=int(i[3]))
    estacion.save()
"""











