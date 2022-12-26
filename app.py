import json
from flask import  Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import nltk #lenguaje natural
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy 
import tensorflow
import tflearn
import random
import pandas as pd
import numpy as np
import markdown
import time
import pickle
from pandas.io.json import json_normalize
from twilio.rest import Client
# from waitress import serve
import subprocess
from pydub import audio_segment
from enviar_email import *

# from Item import *
nltk.download('punkt')

app = Flask(__name__)

respu=[]
cod=[]

@app.route('/')
def hello():
	print("siiii")
	return ("Services chatbot up")

def getData(msg, num):
	df = pd.DataFrame({'Mensaje': [msg], 'Numero': [num]})
	df.to_csv('mensajes.csv', mode='a', index=False, header=False)
	return "ok"

@app.route("/sms", methods=['POST'])

def sms_reply():
	#responde a las llamadas entrantes con un simple mensaje de texto
	# capta el mensaje
	men = []
	global msg
	msg = request.form.get('Body')
	num = request.form.get('From')
	audio = request.form.get('MediaUrl0')
	print(audio)
	print(num)
	print(msg)

	resp = MessagingResponse()
	msgs = resp.message()
	print(msg)

	responded = False

	getData(msg, num)
	men.append(msg)

	NumeroCliente = num

	if len(cod)<1:
		print("nada")
	else:
		codigo_ResP=cod[0]
		msg= (codigo_ResP + msg)

		print(codigo_ResP,"ññññññññññññññññññññññññññ")


	if len(respu) < 1:
		print ("nada")

	else:
		msg = respu[-1]
		print(msg,"oooooooooooooooooo")



		
	if audio == None:
		msg = msg

	else:
		urls = audio
		print(urls, "hhhhhhhhhhhhhhh")

		myfile = requests.get(urls)

		y = myfile.content
		
		open('C:/Users/angieolarte/Downloads/codigo/Angie/audio.opus', 'wb').write(myfile.content)

		command = "ffmpeg -i C:/Users/angieolarte/Downloads/codigo/Angie/audio.opus -ab 160k -ac 2 -ar 44100 -vn C:/Users/angieolarte/Downloads/codigo/Angie/audio.wav"
		subprocess.call(command, shell=True)

		r = sr.Recognizer()

		with sr.AudioFile("C:/Users/angieolarte/Downloads/codigo/Angie/audio.wav") as source:
			audio = r.listen(source)

			text = r.recognize_google(audio, language="es-Es")

		print(text, "tttttttttttttttttttttt")

		msg = text

	cod.clear()

	with open("contenidoRed.json", 'r', encoding="utf-8") as archivo:
		datos = json.load(archivo)
	try:
		with open("variables.pickle", "rb") as archivoPickle:
			palabras, tags, entrenamiento, salida = pickle.load(archivoPickle)
	except:
		palabras=[]
		tags=[]
		auxX=[] #auxiliares 
		auxY=[]
		for contenido in datos["contenido"]:
			for patrones in contenido["patrones"]: #acceder a cualquier elemento
				auxPalabra = nltk.word_tokenize(patrones) #separar palabras Reconocer puntos especiales
				palabras.extend(auxPalabra)
				auxX.append(auxPalabra)
				auxY.append(contenido["tag"])
				if contenido["tag"] not in tags:	
					tags.append(contenido["tag"])
	#Entranamiento aprendizaje automatico
		palabras = [stemmer.stem(w.lower())for w in palabras if w!="?"]#pasar todas las palabras en minuscular
		palabras = sorted(list(set(palabras)))
		tags = sorted(tags)
		entrenamiento = []
		salida=[]
		salidaVacia = [0 for _ in range(len(tags))]
		for x, documento in enumerate(auxX):
			cubeta=[]
			auxPalabra=[stemmer.stem(w.lower()) for w in documento]
			for w in palabras:
				if w in auxPalabra:
					cubeta.append(1)	
				else:
					cubeta.append(0)
			filaSalida = salidaVacia[:]	
			filaSalida[tags.index(auxY[x])]=1
			entrenamiento.append(cubeta)
			salida.append(filaSalida)
	#Definición redes neuronales a utilizar
		entrenamiento = numpy.array(entrenamiento)
		salida = numpy.array(salida)

		with open ("variables.Pickle", "wb") as archivoPickle:
			pickle.dump((palabras, tags, entrenamiento, salida), archivoPickle)

	tensorflow.reset_default_graph()
	red = tflearn.input_data(shape=[None,len(entrenamiento[0])])
	red = tflearn.fully_connected(red,100)
	red = tflearn.fully_connected(red,len(salida[0]),activation="softmax")
	red = tflearn.regression(red) #probabilidades
	modelo = tflearn.DNN(red)
	try: 
		modelo.load("modelo.tflearn")
	except:
		modelo.fit(entrenamiento,salida,n_epoch=1000,batch_size=100,show_metric=True) #bactch_size es la cantidad de neuronas en la red 
		modelo.save("modelo.tflearn")

	entrada = str(msg)
	cubeta = [0 for _ in range(len(palabras))]
	entradaProcesada = nltk.word_tokenize(entrada)
	entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
	for palabraIndividual in entradaProcesada:
		for i,palabra in enumerate(palabras):
			if palabra == palabraIndividual:
				cubeta[i]=1
	resultados =modelo.predict([numpy.array(cubeta)])
	resultadosIndices = numpy.argmax(resultados)
	global tag
	tag = tags[resultadosIndices]

	respu.clear()

	print(tag)

	for tagAux in datos["contenido"]:
		if tagAux["tag"] == tag:
			print(tagAux["tag"], "no se que es ")
			respuest =tagAux["respuesta"]
			codi =tagAux["codigo"]
			respuesta=respuest[0]

			print(respuesta)

			msgs.body(respuesta)
			responded = True

			codig =codi[0]
			cod.append(codig)
			print(codig, "este es el codigo")
			

			

			with open("correos.json") as archivo:
				datos = json.load(archivo)

			# for f in datos['usuarios']:
			# 	g = f['numero']
			# 	if num == g:
			# 		correos = f['correo']
			# 		print(correos, "este es mi correo")

			# 		envia = CorreoDesprendible(correos, texto)
			# else:
			# 	print("no hay correo")

			if tagAux["tag"] == "Informes":
				respu.append("distrito")

			elif tagAux["tag"] == "Archivos de programas":
				respu.append("distrito")

			elif tagAux["tag"] == "distrito":
				respu.append("estacion")

			elif tagAux["tag"] == "estacion":
				with open("correos.json") as archivo:
					datos = json.load(archivo)
	
				for f in datos['usuarios']:
					g = f['numero']
					if num == g:
						correos = f['correo']
						print(correos, "este es mi correo")

						envia = CorreoDesprendible(correos)

			else:
				print("nada")
	
	return str(resp)
if __name__ == "__main__":
	app.run(debug=True)

