import socket
from tkinter import *

PORT = 52245
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
message = client.recv(1024).decode(FORMAT)
print(message)

class GuiForClient:
    root = Tk()