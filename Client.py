import socket
from tkinter import *
import pickle


port = 52245
server = "127.0.0.1"
address = (server, port)
format = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)

class LoginGUI:
    def __init__(self):
        # initialisere tkinter og tilføjere egenskaber til vinduet.
        self.root = Tk()
        self.root.withdraw()
        self.login_window = Toplevel()
        self.login_window.title("Login")
        self.login_window.geometry("300x250")
        self.login_window.resizable(False, False)
        # tilføjer username og password label med en boks man kan skrive i
        self.username = Label(self.login_window, text="Username")
        self.username.place(x=40, y=40)
        self.usernameEntry = Entry(self.login_window)
        self.usernameEntry.place(x=100, y=42)
        self.password = Label(self.login_window, text="Password")
        self.password.place(x=40, y=65)
        self.passwordEntry = Entry(self.login_window, show="*")
        self.passwordEntry.place(x=100, y=67)
        # tilføjer 2 knapper til login og registrer
        self.loginB = Button(self.login_window, text="Login", pady=5, padx=30, command=lambda: self.login(), width=5)
        self.loginB.place(x=100, y=100)
        self.registerB = Button(self.login_window, text="Register", pady=5, padx=30,
                                command=lambda: self.register(), width=5)
        self.registerB.place(x=100, y=150)
        self.login_window.mainloop()

    def popup_message(self, text):
        popup = Toplevel()
        popup.title("Error")
        popup.resizable(0, 0)
        label_popup = Label(popup, text=text)
        label_popup.pack()
        ok_button = Button(popup, text="OK", command=lambda: popup.destroy())
        ok_button.pack()

    def register(self):
        client.send(pickle.dumps([self.usernameEntry.get(), self.passwordEntry.get(), "register"]))

        #message = client.recv(1024).decode(format)
        #print(message)

    def login(self):
        print("test")
        #client.send(pickle.dumps([self.usernameEntry.get(), self.passwordEntry.get(), "login"]))
        #message = client.recv(1024).decode(format)

class ClientGui:
    def __init__(self):






client = LoginGUI()
