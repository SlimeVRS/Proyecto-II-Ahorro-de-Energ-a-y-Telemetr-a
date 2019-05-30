from tkinter import *
from threading import Thread
import threading
import os
import time      
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
from WiFiClient import NodeMCU

root=Tk()
root.title('Proyecto II')
root.minsize(800,400)
root.resizable(width=NO,height=NO)

C_root=Canvas(root, width=800,height=600)
C_root.place(x=0,y=0)

L_Titulo = Label(C_root,text="Mensajes Enviados",font=('Arial',14),fg='black')
L_Titulo.place(x=100,y=5)

L_Titulo = Label(C_root,text="Respuesta Mensaje",font=('Arial',14),fg='black')
L_Titulo.place(x=490,y=5)

SentCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
SentCarScrolledTxt.place(x=10,y=40)

RevCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
RevCarScrolledTxt.place(x=400,y=40)

myCar = NodeMCU()
myCar.start()


def get_log():
    """
    Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
    """
    indice = 0
    # Variable del carro que mantiene el hilo de escribir.
    while(myCar.loop):
        while(indice < len(myCar.log)):
            mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
            SentCarScrolledTxt.insert(END,mnsSend)
            SentCarScrolledTxt.see("end")

            mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
            RevCarScrolledTxt.insert(END, mnsRecv)
            RevCarScrolledTxt.see('end')

            indice+=1
        time.sleep(0.200)
    
p = Thread(target=get_log)
p.start()
           
L_Titulo = Label(C_root,text="Comandos:",font=('Arial',14),fg='black')
L_Titulo.place(x=330,y=250)


L_Titulo = Label(C_root,text="Sense; \t \t \t Infinite;",font=('Arial',14),fg='black')
L_Titulo.place(x=220,y=280)

L_Titulo = Label(C_root,text="ZigZag; \t \t \t Indeciso;",font=('Arial',14),fg='black')
L_Titulo.place(x=220,y=310)

L_Titulo = Label(C_root,text="Parpadeo; \t \t girarFacil;",font=('Arial',14),fg='black')
L_Titulo.place(x=220,y=340)


L_Titulo = Label(C_root,text="Mensaje:",font=('Arial',14),fg='black')
L_Titulo.place(x=100,y=210)

E_Command = Entry(C_root,width=30,font=('Arial',14))
E_Command.place(x=200,y=210)


def send (event):
    """
    Ejemplo como enviar un mensaje sencillo sin importar la respuesta
    """
    mns = str(E_Command.get())
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        myCar.send(mns)
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')") 


def sendShowID():
    """
    Ejemplo como capturar un ID de un mensaje específico.
    """
    mns = str(E_Command.get())
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        mnsID = myCar.send(mns)
        messagebox.showinfo("Mensaje pendiente", "Intentando enviar mensaje, ID obtenido: {0}\n\
La respuesta definitiva se obtine en un máximo de {1}s".format(mnsID, myCar.timeoutLimit))
        
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

def read():
    """
    Ejemplo de como leer un mensaje enviado con un ID específico
    """
    mnsID = str(E_read.get())
    if(len(mnsID)>0 and ":" in mnsID):
        mns = myCar.readById(mnsID)
        if(mns != ""):
            messagebox.showinfo("Resultado Obtenido", "El mensaje con ID:{0}, obtuvo de respuesta:\n{1}".format(mnsID, mns))
            E_read.delete(0, 'end')
        else:
            messagebox.showerror("Error de ID", "No se obtuvo respuesta\n\
El mensaje no ha sido procesado o el ID es invalido\n\
Asegurese que el ID: {0} sea correcto".format(mnsID))

    else:
        messagebox.showwarning("Error en formato", "Recuerde ingresar el separador (':')")

root.bind('<Return>', send) #Vinculando tecla Enter a la función send

Btn_ConnectControl = Button(C_root,text='Enviar',command=lambda:send(None),fg='white',bg='black', font=('Arial',12))
Btn_ConnectControl.place(x=550,y=210)

root.mainloop()
