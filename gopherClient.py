import socket
import os

clear = lambda: os.system('cls')

def printBuffer(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("gopher.floodgap.com", 70))
    s.send(request.encode("UTF-8"))
    buffer = s.recv(1024)
    while len(buffer) > 0:
        print(buffer.decode("UTF-8"))
        buffer = s.recv(1024)
        


# printBuffer("\r\n")
printBuffer("v2/vs?\tedu\r\n")


