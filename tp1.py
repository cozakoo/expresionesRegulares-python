from flask import Flask, render_template # Framework que facilitar el desarrollo de Aplicaciones Web bajo el patrón MVC.

import requests  # importamos libreria
import feedparser
import re # libreria de expresiones regulares
import webbrowser # para abir el navegador directamente

#OBTENEMOS EL HTML
url = 'https://www.imdb.com/search/name/?gender=male,female&start=1&ref_=rlm'
respuesta = requests.get(url)
html = respuesta.text
app = Flask(__name__) 

# https://www.youtube.com/watch?v=fxavwHPJ36o
# Routes to Render Something
@app.route('/')
def home(): 
    return render_template("home.html")


# EXPRESION REGULAR = https://regex101.com/r/GbWqqc/1
# Documentacion ER Python https://docs.python.org/es/3/library/re.html

@app.route('/litacelebridades')
def listarCelebridades():
    global url
    url = 'https://www.imdb.com/search/name/?gender=male,female&start=1&ref_=rlm'
    respuesta = requests.get(url)
    html = respuesta.text
    patron = re.findall(r'<h3.*>\n.*<span.*>(.*)\s<\/span>\n<a.*\n>\s(.*)\n</a>.*<\/h3>\n.*<p.*>\n\s+(.*)\s<span.*>.*<\/span>\n<a.*\n>\s(.*?)\n<\/a>',html)
    print("\nurl inicial: " + str(url))
    return render_template("lista.html", celebridades=patron, url=url)

@app.route('/litacelebridadesSig')
def listarCelebridadesSig():
    global url
    numUrl = re.search(r'(\d+)',url) #obtengo el numero de inicio de famosos. ej 1 - 51 - 151 - 201 etc
    print("\nurl actual: " + str(url))
    proxNumUrl = ((int(50) + int(numUrl.group(0))))  # incremento el numero de famoso que mostrara primero en la lista
    #obtengo la nueva url
    nuevaUrl = re.sub(r'(\d+)',str(proxNumUrl), url, 0) # sustituyo el numero. ej reemplazo el 51 por el 151
    print("\nnueva url : " + str(nuevaUrl))
    respuesta = requests.get(nuevaUrl)
    htmlNueva = respuesta.text  #html de la nueva url
    #asignarURL(nuevaUrl, htmlNueva)
    url = nuevaUrl # asignamos nuestra nueva url
    patron = re.findall(r'<h3.*>\n.*<span.*>(.*)\s<\/span>\n<a.*\n>\s(.*)\n</a>.*<\/h3>\n.*<p.*>\n\s+(.*)\s<span.*>.*<\/span>\n<a.*\n>\s(.*?)\n<\/a>',htmlNueva)
    print()
    return render_template("lista.html", celebridades=patron, url=url)

@app.route('/litacelebridadesAnt')
def listarCelebridadesAnt():
    global url
    numUrl = re.search(r'(\d+)',url) #obtengo el numero de inicio de famosos. ej 1 - 51 - 151 - 201 etc
    # if int(numUrl.group(0))  > int(1) :  # si es otra url que no sea la principal
    numUrlActual = int(numUrl.group(0))
    print("\nurl actual: " + str(url))
    if numUrlActual == 1:
        proxNumUrl = numUrlActual     #actualizo la misma url
        print("\nNO decremento")
    else:
        print("\nDecremento el numero de la url") 
        proxNumUrl = (numUrlActual - int(50) ) #decremento en 50 nuestra url para obtener utl anterior
    
    nuevaUrl = re.sub(r'(\d+)',str(proxNumUrl), url, 0)
    print("\nnueva url : " + str(nuevaUrl))
    respuesta = requests.get(nuevaUrl)
    html = respuesta.text
    url = nuevaUrl
    print()
    patron = re.findall(r'<h3.*>\n.*<span.*>(.*)\s<\/span>\n<a.*\n>\s(.*)\n</a>.*<\/h3>\n.*<p.*>\n\s+(.*)\s<span.*>.*<\/span>\n<a.*\n>\s(.*?)\n<\/a>',html)
    return render_template("lista.html", celebridades=patron, url=url)

webbrowser.open("http://localhost:5000/")
#se segura de que se esta ejecutando este archivo
if __name__ == '__main__':
    app.run()
    # app.run(debug=True) # modo de prueba