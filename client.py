import socket
import threading
from tkinter import *
HEADER = 2048
PORT=5050
SERVER="192.168.137.1"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"



client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def printchat(strmsglist):
   strmsglist = strmsglist.replace("[","").replace("(","").replace("]","").replace("'","").replace("),","\n").replace(",",": ").replace(")","")
   return(strmsglist)
        
def recieve():
    msg_length = client.recv(HEADER).decode(FORMAT)
    msglist = ""
    if msg_length:
        msglist = client.recv(int(msg_length)).decode(FORMAT)
    print(printchat(msglist))
    updatechatTk(printchat(msglist))

def send(msg):
    mes = msg.encode(FORMAT)
    msg_length = len(mes)
    send_length = str(msg_length).encode(FORMAT) 
    send_length += b" "*(HEADER-len(send_length))
    client.send(send_length)
    client.send(mes)


def sendThread():
    while True:
        chat = input("")
        send(chat)
        if chat == DISCONNECT_MSG: break

def receiveThread():
    while sendt.is_alive():
        recieve()

def updatechatTk(chat):
    displayVar.set(chat)

def sendchat(event):
    send(Textbox.get(1.0, END+"-1c"))
    Textbox.delete(1.0, END+"-1c")


try:
    client.send((input("Please enter a username >> : ")).encode(FORMAT))
    sendt = threading.Thread(target=sendThread)
    sendt.start()
    threading.Thread(target=receiveThread).start()
    
    #----------------- CHECK IF THIS IS VALID___________________
    chat = "Welcome!"
    root = Tk()
    root.geometry("500x600")
    root.bind('<Return>',sendchat)
    displayVar = StringVar()
    displayVar.set(chat)
    displayLab = Label(root, textvariable=displayVar)
    displayLab.grid(row=0)

    Textbox = Text(root, height=2)
    Textbox.grid(row=2,)
    # butt = Button(root,command=sendchat,text="Send")
    # butt.grid(row=3,)
    mainloop()
    #______________________________________________________





except threading.ThreadError as e:
    print("An error occured please try reconnecting")
finally:
    if not (sendt.is_alive()):
        client.close()

