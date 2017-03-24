from django.db import models
from geo.models import *

class Estacion(models.Model):
    indicativo =  models.CharField(max_length=40)
    nombre = models.CharField(max_length=70)
    provincia = models.ForeignKey(Provincia)
    ciudad = models.ForeignKey(Ciudad)
    altitud = models.IntegerField()
    
    def __str__(self):
        return "Estacion: " + str(self.ciudad)

class Registro(models.Model):
    estacion = models.ForeignKey(Estacion)
    fecha = models.DateField()
    tmed = models.FloatField()
    prec = models.FloatField()
    tmin = models.FloatField()
    hora_tmin = models.DateField()
    tmax = models.FloatField()
    hora_tmax = models.DateField()
    direction = models.FloatField()
    vel_media = models.FloatField()
    racha = models.FloatField()
    hora_racha= models.DateField()
    sol = models.FloatField()
    pres_max = models.FloatField()
    pres_min = models.FloatField()
    hora_pres_min = models.DateField()
    hora_pres_max = models.DateField()
    
    def __str__(self):
        return self.estacion + " | " + self.fecha

