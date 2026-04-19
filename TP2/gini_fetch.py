import requests
import ctypes

#API URL para obtener los datos de GINI
URL = ("https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI"
    "?format=json&date=2011:2020&per_page=32500&page=1")


#Cargar la librería de C
libgini = ctypes.CDLL("./libgini.so")
libgini.convert_and_sum.argtypes = [ctypes.c_float]
libgini.convert_and_sum.restype = ctypes.c_int

#Consultar la API
response = requests.get(URL)
data = response.json()

registros = data[1]

for r in registros:
    if r["countryiso3code"] == "ARG" and r["value"] is not None:
        value = r["value"]
        result = libgini.convert_and_sum(ctypes.c_float(value))
        print(f"Año: {r['date']} | GINI: {r['value']} | Resultado C: {result}")