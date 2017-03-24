from django.db import models

class Pais(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Provincia(models.Model):
    nombre = models.CharField(max_length=70)
    pais = models.ForeignKey(Pais)
    
    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    provincia = models.ForeignKey(Provincia)
    
    def __str__(self):
        return self.nombre

    

