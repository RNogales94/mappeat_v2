"""
Este script es el encargado de inicializar la base de datos de meteorología para España con los datos de AEMET
"""


from meteo.models import *



API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4cm5vZ2FsZXNAZ21haWwuY29tIiwianRpIjoiMWU4ODU0ZjQtNjM0ZC00ZDhlLWE0NGEtMTQ1ZjUwODUzY2VlIiwiZXhwIjoxNDk3MjI1OTk1LCJpc3MiOiJBRU1FVCIsImlhdCI6MTQ4OTQ0OTk5NSwidXNlcklkIjoiMWU4ODU0ZjQtNjM0ZC00ZDhlLWE0NGEtMTQ1ZjUwODUzY2VlIiwicm9sZSI6IiJ9.b04oCRFuxgxFq7BDzZqT_cY39an6tKF23J7Ee-kl5dA"
