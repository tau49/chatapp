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

        # message = client.recv(1024).decode(format)
        # print(message)

    def login(self):
        print("test")
        client.send(pickle.dumps([self.usernameEntry.get(), self.passwordEntry.get(), "login"]))
        message = client.recv(1024).decode(format)
        if message == 'Login success':
            self.login_window.destroy()
            clientgui = ClientGui()
            clientgui.run_gui()
        elif message == 'Login failed':
            self.popup_message("Login failed either your username or password is wrong")


class ClientGui:
    def __init__(self):
        self.client_gui = Tk()
        # self.client_gui.title("Chatroom")
        # self.client_gui.geometry("300x250")
        # self.client_gui.resizable(False, False)
        self.input_user = StringVar()
        self.input_field = Entry(self.client_gui, text=self.input_user)
        self.input_field.pack(side=BOTTOM, fill=X)
        self.messages = Text(self.client_gui)
        self.messages.yview_pickplace("end")
        self.messages.pack(side=LEFT, fill=Y)
        self.scrollbar = Scrollbar(self.client_gui)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.messages.yview)
        self.frame = Frame(self.client_gui)  # , width=300, height=300)
        self.input_field.bind("<Return>", self.enter_pressed)
        self.frame.pack()
        self.menubar = Menu(self.client_gui)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=lambda: self.hello())
        self.filemenu.add_command(label="Save", command=lambda: self.hello())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=lambda: self.end_session())
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.client_gui.config(menu=self.menubar)

    def hello(self):
        print("Hello")

    def end_session(self):
        #client.send('!exit'.encode("utf-8"))
        self.client_gui.quit()

    def enter_pressed(self, event):
        self.input_get = self.input_field.get()
        self.messages.insert(INSERT, '%s\n' % self.input_get)
        self.input_user.set('')
        self.messages.yview_pickplace("end")
        return "break"

    def run_gui(self):
        print("Starting GUI")
        self.client_gui.mainloop()


class AdminGui(ClientGui):
    def __init__(self):
        super().__init__()
        self.filemenu.add_command(label="Admin", command=self.hello())
        self.client_gui.config(menu=self.menubar)



client = LoginGUI()

#client = ClientGui()
#client.run_gui()
