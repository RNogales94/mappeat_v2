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
    tmed = models.FloatField(null=True)
    prec = models.FloatField(null=True)
    tmin = models.FloatField(null=True)
    hora_tmin = models.TimeField(null=True)
    tmax = models.FloatField(null=True)
    hora_tmax = models.TimeField(null=True)
    direction = models.FloatField(null=True)
    vel_media = models.FloatField(null=True)
    racha = models.FloatField(null=True)
    hora_racha= models.TimeField(null=True)
    sol = models.FloatField(null=True)
    pres_max = models.FloatField(null=True)
    pres_min = models.FloatField(null=True)
    hora_pres_min = models.TimeField(null=True)
    hora_pres_max = models.TimeField(null=True)
    
    def __str__(self):
        return str(self.estacion) + " | " + str(self.fecha)

