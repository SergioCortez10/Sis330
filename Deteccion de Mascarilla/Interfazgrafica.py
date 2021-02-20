from tkinter import *

raiz=Tk()
raiz.title("Detector de mascarilla")
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
raiz.mainloop()