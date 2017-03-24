import urllib.request
from pprint import pprint
import ssl
import json

from geo.models import *
from meteo import AEMET


ssl._create_default_https_context = ssl._create_unverified_context
url  = urllib.request.urlopen("https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/?api_key="+AEMET.API_KEY) 


data = json.loads(url.read())
meteo = urllib.request.urlopen(data['datos'])
meteo =  str(meteo.read(), 'latin-1')  #Pasamos a unicode para que no haya problemas con la Ñ de A CORUÑA
meteoJSON = json.loads(meteo)

provincias = [meteoJSON[item]['provincia'] for item in range(0, len(meteoJSON))]
provincias_sin_repetidos = []
for i in provincias:
    if i not in provincias_sin_repetidos:
        provincias_sin_repetidos.append(i)

#print(provincias_sin_repetidos)
provincias = provincias_sin_repetidos

for i in provincias:
    provincia = Provincia(nombre=str(i), pais=Pais.objects.get(nombre="España"))
    provincia.save()














