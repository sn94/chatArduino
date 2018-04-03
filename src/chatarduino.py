# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


import serial
import threading
import time 
import tkinter 
from tkinter import * 

prefijo="94"
mylist=None
#ventana
tk= None

#widgets
txtmensaje = None

#boton inicio conexion
iniChat= None

#imagen
send=None 


#hilo que se encarga de leer mensajes entrantes
subprocess = None

# conexion serial
arduinoPort=None



    
def iniciar_chat():
    # Iniciando conexión serial
    try:
        global arduinoPort
        arduinoPort = serial.Serial('COM3', 9600, timeout=1)
        # Reset manual del Arduino
        arduinoPort.setDTR(False)  
        time.sleep(0.3)
	# Se borra cualquier data que haya quedado en el buffer
        arduinoPort.flushInput()
        arduinoPort.setDTR()  
        time.sleep(0.3)
        print( "Conectado al puerto com3!")
        # Retardo para establecer la conexión serial
        time.sleep(1.8) 
    except:
        print( "No se puede conectar al puerto COM3")
        global iniChat
        if iniChat:
            iniChat.config(state=NORMAL)



def terminar_chat():
    # Cerrando puerto serial
    global arduinoPort
    if arduinoPort:
        if arduinoPort.isOpen():
            arduinoPort.close()
            print("Puerto com3 cerrado")
            global iniChat
            iniChat.config(state=NORMAL)
        else:
            print("El puerto serial ya fue liberado antes")
    else:
        print("No se puede liberar el puerto, ni siquiera se ha establecido conexion")
            
    

    
def tecla(event):
    if(event.char and len(event.char)==1):
        if ord(event.char) == 13:
            enviar_mensaje()
    
def recibir_mensaje():
    global arduinoPort
    if arduinoPort != None:
        while arduinoPort.isOpen():
            getSerialValue = arduinoPort.readline()
            if not getSerialValue:
                print("Sin datos")
            else:
                strRecibido=  getSerialValue.decode("utf-8")
                if(strRecibido[0:2]!= prefijo): #cuando no se trate de un mensaje propio
                    varr= strRecibido[2:]
                    cargar_mensajes( varr)
            #print(threading.current_thread().getName(), threading.active_count())
            time.sleep(0.1)

def enviar_mensaje():
    mensaje = txtmensaje.get()
    if mensaje=="":
        print("Ingrese su mensaje")
    else:
        global arduinoPort
        if arduinoPort:
            if arduinoPort.isOpen():
                #agregar prefijo de mensaje enviado
                mensajeprefix= prefijo +mensaje

                try:
                    arduinoPort.write(mensajeprefix.encode())
                    txtmensaje.delete(0, len(mensaje) )
                    cargar_mensajes("Tu: "+mensaje)
                except:
                    print("El puerto COM3 no esta disponible para recibir datos")
            else:
                print("El puerto esta cerrado")
        else:
            print("El puerto COM3 no esta disponible para enviar datos")


def crear_receiver():
    subprocess = threading.Thread(
                                  name="receiver",
                                  target=recibir_mensaje,
                                  daemon=False)
    subprocess.start()



def crear_panel_titulo():
    #panel titulo
    panelTitular = Frame(tk, bg="#00796B", width="480", padx="30", pady="65")
    labelTitulo = Label(panelTitular, bg="#00796B", fg="#FFFFFF",
                        text="Simulaciones (Examen Final)\n Python y Arduino",
                        font="Courier 20 bold"
                        )
    labelTitulo.pack()
    
    #panel datos del puerto
    panelPuerto= Frame(panelTitular, bg="#00796B" )
    if arduinoPort!=None: 
        lpuerto= Label(panelPuerto,text= "Conectado a "+arduinoPort.name)
    else:
        lpuerto= Label(panelPuerto,text= "No conectado")
        
    lpuerto.pack()
        
    panelPuerto.pack()
    
    global iniChat
    estadoB=DISABLED
    if not arduinoPort: estadoB= NORMAL
    iniChat= Button(panelTitular,text="iniciar",command=iniciar_chat,state= estadoB,
    font="Courier 14 italic",fg="#5555ff")
    iniChat.pack(side="left")
    
    estadoB1= NORMAL
    if not arduinoPort: estadoB1= DISABLED
    endChat= Button(panelTitular,text="cerrar",command=terminar_chat,
    font="Courier 14 italic",fg="#5555ff", state= estadoB1)
    endChat.pack(side="right")
    panelTitular.pack(side="top")
    
    
    
def crear_panel_form():
    #panel superior
    panelTop = Frame(tk, bg="#00796B", pady="10", padx="10")
    # campo de texto
    global txtmensaje
    txtmensaje = Entry(panelTop, width="20", font="Calibri 28", bd="3",
                       fg="#212121")
    txtmensaje.bind("<Key>", tecla)
    txtmensaje.pack(side="left")
    
    # boton de envio
    global send
    send = PhotoImage(file="send.png")
    enviar = Button(panelTop, image=send, height="50", bd="0", bg="#00796B",
                    activebackground="#FFCCBC",
                    command=enviar_mensaje)
    enviar.pack(side="right")

    panelTop.pack(side="top")
    
    
def crear_scroll():
    scrollbar = Scrollbar(tk)
    scrollbar.pack( side = RIGHT, fill = Y )
    global mylist
    mylist = Listbox(tk, width=100,
    yscrollcommand=scrollbar.set,
    font="Courier 18",highlightcolor="#00ff00",selectbackground="pink",selectforeground="black")
    #for line in range(100):
       #mylist.insert(END, "This is line number " + str(line))

    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config( command = mylist.yview )

   
def cargar_mensajes(arg):
    global mylist
    mylist.insert(END, arg)
    
def crear_ventana():
    tk = Tk()
    tk.config(bg="#00796B")
    tk.geometry("500x500")
    tk.title("Chat de arduinos")
    crear_panel_titulo()
    crear_panel_form()
    #crear_panel_mensajes() 
    crear_scroll()
    tk.mainloop()
    #help("modules")
    
    
if __name__ == "__main__":
    
    
    iniciar_chat()
    crear_ventana()
    crear_receiver()