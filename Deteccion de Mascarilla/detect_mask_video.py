# importar paquetes necesarios
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np

import imutils
import time
import cv2
import os

from tkinter import *

raiz=Tk()
raiz.title("Detector de mascarilla")
raiz.geometry("1200x600")
raiz.iconbitmap("icono.ico")

miFrame = Frame(raiz , width=1200 , height =600)
miFrame.pack()
Imagen=PhotoImage(file="1.png")
Imagen2=PhotoImage(file="2.png")

Label(miFrame, text= "Detector de mascarilla" , fg = "black" , font =("Comic Sans MS",20)).place(x = 300, y = 0)
Label(miFrame, text= "Necesita utilizar la mascarilla correctamente para ingresar verificacion : " , fg = "black" , font =("Comic Sans MS",14)).place(x = 0 , y = 40)
Label(miFrame, image=Imagen2).place(x=120, y=120)
Label(miFrame, text= "Uso correcto de mascarilla" , fg = "green" , font =("Comic Sans MS",15)).place(x = 300, y = 158)
Label(miFrame, image=Imagen).place(x=120, y=320)
Label(miFrame, text= "Uso incorrecto de la mascarilla" , fg = "red" , font =("Comic Sans MS",15)).place(x = 300, y = 365)



def detect_and_predict_mask(frame, faceNet, maskNet):
	

	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)



	faces = []
	locs = []
	preds = []


# bucle sobre las detecciones
	for i in range(0, detections.shape[2]):
		

		confidence = detections[0, 0, i, 2]
		#filtro las detecciones débiles asegurándose de que la confianza sea
		#mayor que la confianza mínima
		if confidence > 0.5:
			

			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			

			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)
		

			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# predicciones si se detectó al menos un rostro
	if len(faces) > 0:
		
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	return (locs, preds)

#cargue nuestro modelo de detector facial serializado desde el disco
print("[INFO] loading face detector model...") 
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath =r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

#Cargar el modelo
print("[INFO] loading face mask detector model...")
maskNet = load_model("mask4_detector.model")


print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()


while True:
	
	frame = vs.read()
	frame = imutils.resize(frame, width=400)


	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)


	for (box, pred) in zip(locs, preds):
		
		# desempaqueta el cuadro delimitador y las predicciones
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred
	

		#label = "Mascarilla" if mask > withoutMask else "No lleva Mascarilla"
		#color = (0, 255, 0) if label == "LLeva Mascarilla" else (0, 0, 255)
		if(withoutMask>mask):
			label = "No lleva mascarrilla"		
		else:
			label = "Mascarilla"
				
			
		if(label == "No lleva mascarrilla"):
			color = (0, 0, 255)
		if(label == "Mascarilla"):
			color = (0, 255, 0)
		

		# incluye la probabilidad en la etiqueta
		label = "{}: {:.3f}%".format(label, max(mask, withoutMask) * 100)

		cv2.putText(frame, label, (startX, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

	#muestra el cuadro de salida
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()