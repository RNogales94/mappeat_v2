"""
NOTA:
Este script debe ejecutarse una unica vez para inicializar la base de datos
La forma correcta de ejecutarlo es mediante: python3 manage.py < meteo/initCiudades.py
"""

import urllib.request
from pprint import pprint
import ssl
import json
import time

from dateutil import parser
import datetime

from geo.models import *
from meteo.models import *
from meteo import AEMET


ssl._create_default_https_context = ssl._create_unverified_context

estaciones = Estacion.objects.all()
#estacion = Estacion.objects.all()[0]

for estacion in estaciones:
    INDICATIVO = estacion.indicativo
    print(estacion.indicativo)
    #Indent:
    FECHAINI = "2017-01-01T00%3A00%3A00UTC"
    FECHAFIN = "2017-01-05T00%3A00%3A00UTC"
    try:
        url  = urllib.request.urlopen("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/"+FECHAINI+"/fechafin/"+FECHAFIN+"/estacion/"+INDICATIVO+"/?api_key="+AEMET.API_KEY) 
    except urllib.error.HTTPError:
        print("ERROR AEMET CATCHED.. Esperamos 20 seg y repetimos")
        time.sleep(21)
        url  = urllib.request.urlopen("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/"+FECHAINI+"/fechafin/"+FECHAFIN+"/estacion/"+INDICATIVO+"/?api_key="+AEMET.API_KEY)
        
    data = json.loads(url.read())
    meteo = urllib.request.urlopen(data['datos'])
    meteo =  str(meteo.read(), 'latin-1')  #Pasamos a unicode para que no haya problemas con las Ñ's etc
    meteoJSON = json.loads(meteo)
    
    try:
        print(meteoJSON[0])
    except KeyError:
        print("KEY ERROR CATCH, LEN=", print(meteoJSON['descripcion']))
    except TypeError:
        print("TYPE ERROR CATCH")
    
    num_dias = len(meteoJSON)
    print("OK")
    

"""














    if estado == "404":
        print("NO HAY DATOS ASOCIADOS A: "+INDICATIVO+" desde "+FECHAINI+" hasta "+FECHAFIN)
    else:
        for registro_diario in range(0, num_dias):
            r = meteoJSON[registro_diario] #Variable auxiliar para hacer mas rapida la escritura
            #ESTACION
            estacion = Estacion.objects.filter(indicativo=r['indicativo'])[0]

            #SOL
            try:
                sol_value = float(r['sol'].replace(',','.'))
            except KeyError:
                sol_value = None

            #PREC
            try:
                if r['prec'] == 'Ip':
                    prec = 0
                else:
                    prec = float(r['prec'].replace(',','.'))
            except KeyError:
                prec = None

            #PresMax
            try:
                pres_max = float(r['presMax'].replace(',','.'))
            except KeyError:
                pres_max = None

            #PresMin
            try:
                pres_min = float(r['presMin'].replace(',','.'))
            except KeyError:
                pres_min = None

            #TMin
            try:
                tmin = float(r['tmin'].replace(',','.'))
            except KeyError:
                tmin = None

            #TMed
            try:
                tmed = float(r['tmed'].replace(',','.'))
            except KeyError:
                tmed = None

            #TMax
            try:
                tmax = float(r['tmax'].replace(',','.'))
            except KeyError:
                tmax = None            

            #HORA TMIN
            try:
                dt = parser.parse(r['horatmin'])
                hora_tmin = datetime.time(dt.hour, dt.minute)
            except ValueError:
                hora_tmin = None
            except KeyError:
                hora_tmin = None

            #HORA TMAX
            try:
                dt = parser.parse(r['horatmax'])
                hora_tmax = datetime.time(dt.hour, dt.minute)
            except ValueError:
                hora_tmax = None
            except KeyError:
                hora_tmax = None

            #HORA PresMIN
            try:
                hora_pmin = datetime.time(int(r['horaPresMin']))
            except ValueError:
                hora_pmin = None
            except KeyError:
                hora_pmin = None

            #HORA PresMAX
            try:
                hora_pmax = datetime.time(int(r['horaPresMax']))
            except ValueError:
                hora_pmax = None
            except KeyError:
                hora_pmax = None

            #DIRECTION
            try:
                direction = float(r['dir'].replace(',','.'))
            except ValueError:
                direction = None
            except KeyError:
                direction = None

            #VEL MEDIA
            try:
                vel_media = float(r['velmedia'].replace(',','.'))
            except ValueError:
                vel_media = None
            except KeyError:
                vel_media = None

            #RACHA
            try:
                racha = float(r['racha'].replace(',','.'))
            except ValueError:
                racha = None
            except KeyError:
                racha = None

            #HORA RACHA  horaracha
            try:
                dt = parser.parse(r['horaracha'])
                horaracha = datetime.time(dt.hour, dt.minute)        
            except ValueError:
                horaracha = None
            except KeyError:
                horaracha = None


            registro_actual = Registro( fecha = parser.parse(r['fecha']),
                                        estacion = estacion,
                                        tmed = tmed,
                                        tmin = tmin,
                                        tmax = tmax,
                                        direction = direction,
                                        racha = racha,
                                        prec = prec,
                                        vel_media = vel_media,
                                        sol = sol_value,
                                        pres_max = pres_max,
                                        pres_min = pres_min,
                                        hora_tmin = hora_tmin,
                                        hora_tmax = hora_tmax,
                                        hora_racha = horaracha,
                                        hora_pres_min = hora_pmin,
                                        hora_pres_max = hora_pmax
                                        )
            registro_actual.save()
    print("OK")
    #Fin del for registros
#Fin del for estaciones





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
