"""
NOTA:
Este script debe ejecutarse una unica vez para inicializar la base de datos
La forma correcta de ejecutarlo es mediante: python3 manage.py < meteo/initCiudades.py
"""

import urllib.request
from pprint import pprint
import ssl
import json

from dateutil import parser
import datetime

from geo.models import *
from meteo.models import *
from meteo import AEMET

def initRegistro(fechaini, fechafin, indicativo)
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

#print(meteoJSON)
"""
CAMPOS DE UN REGISTRO:
  + fecha
  + tmed
  + prec
  + tmin
  + horatmin
  + tmax
  + horatmax
  + dir (Direccion del viento)
  + velmedia
  + racha
  + horaracha
  + sol
  + presMax
  + presMin
  + horapresMax
  + horapresMin

"""
def asPrec(prec):
    if prec == 'Ip':
        prec = 0;
    else:
        prec = float(prec.replace(',','.'))
    return prec

def asSol(sol):
    if sol is None:
        sol = null
    else:
        sol = float(sol.replace(',','.'))
    return sol




num_dias = len(meteoJSON)
for registro_diario in range(0, num_dias):
    r = meteoJSON[registro_diario] #Variable auxiliar para hacer mas rapida la escritura
    #ESTACION
    estacion = Estacion.objects.filter(indicativo=r['indicativo'])[0]
    
    #SOL
    try:
        sol_value = asSol(r['sol'])
    except KeyError:
        sol_value = None
    
    #HORA TMIN
    try:
        dt = parser.parse(r['horatmin'])
        hora_tmin = datetime.time(dt.hour, dt.minute)
    except ValueError:
        hora_tmin = None
    
    #HORA TMAX
    try:
        dt = parser.parse(r['horatmax'])
        hora_tmax = datetime.time(dt.hour, dt.minute)
    except ValueError:
        hora_tmax = None
    
    #HORA PresMIN
    try:
        hora_pmin = datetime.time(int(r['horaPresMin']))
    except ValueError:
        hora_pmin = None
    
    #HORA PresMAX
    try:
        hora_pmax = datetime.time(int(r['horaPresMax']))
    except ValueError:
        hora_pmax = None
        
    registro_actual = Registro( fecha = parser.parse(r['fecha']),
                                estacion = estacion,
                                tmed = float(r['tmed'].replace(',','.')),
                                tmin = float(r['tmin'].replace(',','.')),
                                tmax = float(r['tmax'].replace(',','.')),
                                direction = float(r['dir'].replace(',','.')),
                                racha = float(r['racha'].replace(',','.')),
                                prec = asPrec(r['prec']),
                                vel_media = float(r['velmedia'].replace(',','.')),
                                sol = sol_value,
                                pres_max = float(r['presMax'].replace(',','.')),
                                pres_min = float(r['presMin'].replace(',','.')),
                                hora_tmin = hora_tmin,
                                hora_tmax = hora_tmax,
                                hora_pres_min = hora_pmin,
                                hora_pres_max = hora_pmax
                                )
    registro_actual.save()
    
    
    
    
    #print(float((meteoJSON[registro_diario]['tmed'].replace(',', '.'))))














