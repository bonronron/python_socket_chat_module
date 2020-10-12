import socket 
import threading


HEADER = 2048
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
MSG_LIST = []
ACTIVECONS = set()
CLIENTNAMES = {}
clients_lock = threading.Lock()
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def updatechat():
    for i in ACTIVECONS:
        mes = str(MSG_LIST).encode(FORMAT)
        msg_length = len(mes)
        send_length = str(msg_length).encode(FORMAT) 
        send_length += b" "*(HEADER-len(send_length))
        i.send(send_length)
        i.send(mes) 

def handle_client(conn,addr):
    print("new connection",addr)
    with clients_lock:
        ACTIVECONS.add(conn)
    CLIENTNAMES[addr] = conn.recv(2048).decode(FORMAT)
    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                MSG_LIST.append((CLIENTNAMES[addr],msg))
                updatechat()
                if(msg == DISCONNECT_MSG): connected = False
                
                print(addr,msg)
    finally:
        with clients_lock:
            ACTIVECONS.remove(conn)
            conn.close()
    






def start():
    server.listen()
    print("Server is listening on :", (SERVER,PORT))
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client,args = (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("server is runnning")
start()
