import socket
from tkinter import *


class GuiForClient:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry("300x250")
        self.login.resizable(False, False)
        self.username = Label(self.login, text="Username")
        self.username.place(x=40, y=40)
        self.usernameEntry = Entry(self.login)
        self.usernameEntry.place(x=100, y=42)
        self.password = Label(self.login, text="Password")
        self.password.place(x=40, y=65)
        self.passwordEntry = Entry(self.login, show="*")
        self.passwordEntry.place(x=100, y=67)
        self.loginB = Button(self.login, text="Login", pady=5, padx=30, command=print("login"), width=5)
        self.loginB.place(x=100, y=100)

        self.registerB = Button(self.login, text="Register", pady=5, padx=30, command=print("login"), width=5)
        self.registerB.place(x=100, y=150)
        self.login.mainloop()


# class GuiForAdmin:
#    def __init__(self):


class UserFactory:
    def create_user(self, name):
        print("Test")


client = GuiForClient()

# PORT = 52245
# SERVER = "127.0.0.1"
# ADDRESS = (SERVER, PORT)
# FORMAT = "utf-8"
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDRESS)
# message = client.recv(1024).decode(FORMAT)
# print(message)
