#importo las librerias que voy a usar
import requests
import pandas
import plotly.express as px
import arrow
#Descargo los datos
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson" #la url que voy a usar para pedir los datos
datos = requests.get(url).json() #lo convierto el json que me devuelve el requests y lo transformo en un diccionario

#pasamos los datos del diccionarios a una lista llamada terremotos
terremotos = []
for terremoto in datos["features"]: #por cada terremoto que hay lo meto en terremoto con los datos mas importantes (en el json de los terremotos estan los "features" que se refieren a los terremotos y sus datos)
    datos_terremoto = terremoto["properties"] #creo una variable que tenga todos los datos generales del terremoto
    coordenadas = terremoto["geometry"]["coordinates"] #creo una variable con las cordenadas
    #le añado un diccionario con todos los datos que me sirven para graficar a la lista terremotos 
    terremotos.append({  
        "magnitud": datos_terremoto["mag"], 
        "lugar": datos_terremoto["place"],
        "hora": arrow.get(datos_terremoto["time"] / 1000).format("DD-MM-YYYY HH:mm:ss"), #el tiempo esta en milisegundos contando desde el 1 de enero de 1970 (la época UNIX) use esta libreria para hacerlo mas facil
        "longitud": coordenadas[0],
        "latitud": coordenadas[1]
    })

tabla_terremotos = pandas.DataFrame(terremotos) #hago una tabla con el pandas de todos los terremotos
tabla_terremotos = tabla_terremotos[tabla_terremotos["magnitud"] > 0] #filtro las magnitudes iguales o menores a cero porque no tengo forma de graficarlo

Grafico = px.scatter_geo(
    tabla_terremotos, #le paso la tabla con todos los terremotos y plotly lo grafica
    title="Terremotos del mundo en las ultimas 24 horas 🚫❗⚠🐱‍👤",
    lat="latitud", 
    lon="longitud",
    color="magnitud",
    size="magnitud",
    hover_name="lugar",
    hover_data={"hora": True}, #esto es si le quiero agregar datos (yo solo le puse la hora pero se pueden agragar mas)
    projection="orthographic", #esto es el tipo de mapa del mundo que va a usar
    color_continuous_scale="Bluered" #son los colores de la escala
)

Grafico.show()
