import tkinter as tk
import requests
from tkinter import Scrollbar
import plotly.express as px
import arrow
import pandas as pd
#hago la ventana principal de tkinter
ventana = tk.Tk()
ventana.title("Usuarios y Repositorios")
ventana.geometry("560x315")
#creo la entrada
entrada = tk.Entry(ventana,width= 25)  
entrada.place(x=50,y=75)
#creo un texto
texto = tk.Label(text="Ingresar usuario de Github",font="Arial")
texto.place(x=10,y=25)
#creo una lista para los repositorios
lista_repositorios = tk.Listbox(ventana,width=280,height=19)
lista_repositorios.place(x=280,y=0)
# Creo la barra de desplazamiento
scrollbar = Scrollbar(ventana, orient="vertical", command=lista_repositorios.yview)
scrollbar.place(x=265, y=0, height=315,width=15)
# Conecto la scrollbar con la lista
lista_repositorios.config(yscrollcommand=scrollbar.set)

def obtener_info_repos(): 
    global usuario
    lista_repositorios.delete(0,tk.END)
    usuario = entrada.get()
    url = f"https://api.github.com/users/{usuario}/repos"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        if datos:
            for repositorio in datos:
                lista_repositorios.insert(tk.END,repositorio["name"])
        else:
            lista_repositorios.insert(tk.END, "Este usuario no tiene repos públicos.")        

def obtener_info_plotly(event):
    indice = lista_repositorios.curselection()
    repo = lista_repositorios.get(indice)
    url = f"https://api.github.com/repos/{usuario}/{repo}/languages"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        lenguajes = respuesta.json()
        if lenguajes:
            grafico_lenguajes = px.pie(
                names=lenguajes.keys(),
                values=lenguajes.values(),
                title="Lenguajes utilizados en este repositorio"
            )
            grafico_lenguajes.show()
    else:
        print("Error al obtener lenguajes del repositorio.")
    url = f"https://api.github.com/repos/{usuario}/{repo}/stats/commit_activity"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        commits = respuesta.json()
        if commits:
            ultima_semana = commits[-1]
            dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            fecha = arrow.get(ultima_semana["week"]).format("DD-MM-YYYY")
            grafico_commits = px.bar(
                x=dias,
                y=ultima_semana["days"],
                labels={"x": "Día", "y": "Commits"},
                title=f"Commits en la semana que comienza el {fecha}",
            )
            grafico_commits.show()
    url = f"https://api.github.com/repos/{usuario}/{repo}/contributors"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        contribuidores = respuesta.json()
        if contribuidores:
            top_contribuidores = contribuidores[:10]
            nombres = []
            contribuciones = []
            for contribuidor in top_contribuidores:
                nombres.append(contribuidor["login"])
                contribuciones.append(contribuidor["contributions"])
            
            df_contribuidores = pd.DataFrame({
                "Usuario": nombres,
                "Commits": contribuciones
            })

            grafico_contribuidores = px.funnel(
                df_contribuidores,
                y="Usuario",
                x="Commits",
                title="Top 10 (o menos) contribuidores"
            )
            grafico_contribuidores.show()
#creo el boton
boton = tk.Button(ventana,text="buscar repositorios",width=15,command=obtener_info_repos)
boton.place(x=67,y=100)
lista_repositorios.bind("<Double-1>",obtener_info_plotly)

ventana.mainloop()