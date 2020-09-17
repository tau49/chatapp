import socket
from tkinter import *
import pickle

PORT = 52245
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

class GuiForClient:
    def __init__(self):
        # initialisere tkinter og tilføjere egenskaber til vinduet.
        self.root = Tk()
        self.root.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry("300x250")
        self.login.resizable(False, False)
        # tilføjer username og password label med en boks man kan skrive i
        self.username = Label(self.login, text="Username")
        self.username.place(x=40, y=40)
        self.usernameEntry = Entry(self.login)
        self.usernameEntry.place(x=100, y=42)
        self.password = Label(self.login, text="Password")
        self.password.place(x=40, y=65)
        self.passwordEntry = Entry(self.login, show="*")
        self.passwordEntry.place(x=100, y=67)
        # tilføjer 2 knapper til login og registrer
        self.loginB = Button(self.login, text="Login", pady=5, padx=30, command=print("login"), width=5)
        self.loginB.place(x=100, y=100)
        self.registerB = Button(self.login, text="Register", pady=5, padx=30,
                                command=lambda: self.register(self.usernameEntry.get(), self.passwordEntry.get()), width=5)
        self.registerB.place(x=100, y=150)
        self.login.mainloop()

    def register(self, username, password):
        print(username, password)
        self.username = Label(self.login, text="test")
        self.username.place(x=40, y=40)
        message = pickle.loads(client.recv(1024))
        client.send(pickle.dumps([self.username, self.password]))


        #self.popup = Toplevel()
        #self.popup.title("Login Failed")
        #self.usernamelabel = Label(self.popup, text=username)
        #self.usernamelabel.place(x=40, y=40)
        #self.passwordlabel = Label(self.popup, text=password)
        #½self.passwordlabel.place(x=40, y=65)



client = GuiForClient()
