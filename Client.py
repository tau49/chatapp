import socket
from tkinter import *
import pickle
from threading import Thread

#her opretter klienten forbindelsen til serveren.
port = 52245
server = "192.168.87.104"
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
        # popup metode som jeg bruger senere
        popup = Toplevel()
        popup.title("Error")
        popup.resizable(0, 0)
        label_popup = Label(popup, text=text)
        label_popup.pack()
        ok_button = Button(popup, text="OK", command=lambda: popup.destroy())
        ok_button.pack()

    def register(self):
        # dette bliver brugt til at lave en bruger ved at sende informationen til serveren med en register string
        # måden det så fungere på er at serveren opretter brugeren i databasen og giver så lov til at logge på
        # her bruger jeg så popup metoden til at vise en besked
        client.send(pickle.dumps([self.usernameEntry.get(), self.passwordEntry.get(), "register"]))
        message = client.recv(1024).decode(format)
        if message == 'Username is already in use':
            self.popup_message("this username is already in use please choose another")
        elif message == 'Welcome':
            self.popup_message("User created")
            self.login_window.destroy()
            clientgui = AdminGui()
            clientgui.run_gui()

    def login(self):
        # dette er metoden til at logge på den sender login information til serveren som så tjekker databasen om du har
        # adgang til serveren. klienten modtager så om den får lov og hvis den gør starter den så guien
        self.username = self.usernameEntry.get()
        client.send(pickle.dumps([self.usernameEntry.get(), self.passwordEntry.get(), "login"]))
        message = client.recv(1024).decode(format)
        if message == 'Login success':
            self.login_window.destroy()
            clientgui = AdminGui(self.username)
            clientgui.run_gui()
        elif message == 'Login failed':
            self.popup_message("Login failed either your username or password is wrong")

class ClientGui:
    # dette er klient guien som man ser efter login, det er her chatten kommer til at forgå, det der sker er at den
    # opretter guien ved at bruge tkinter
    def __init__(self, *username):
        self.client_gui = Tk()
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
        self.filemenu.add_command(label="info", command=lambda: self.info())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=lambda: self.end_session())
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.client_gui.config(menu=self.menubar)
        self.username = username

    def popup_message(self, text):
        popup = Toplevel()
        popup.title("Error")
        popup.resizable(0, 0)
        label_popup = Label(popup, text=text)
        label_popup.pack()
        ok_button = Button(popup, text="OK", command=lambda: popup.destroy())
        ok_button.pack()

# afslutter sessionen dette er meningen at den skal blive brugt i fil menuen
    def end_session(self):
        exit()

# dette er et event som registere om enter bliver trykket og når det så gør sender den så beskeden til serveren
# og printer den så i din dialog.
    def enter_pressed(self, event):
        self.input_get = self.input_field.get()
        self.messages.insert(INSERT, '%s\n' % self.input_get)
        self.input_user.set('')
        self.messages.yview_pickplace("end")
        self.input_field.delete(0, 'end')
        client.send(self.input_get.encode(format))

# dette er en metode til at starte gui og starte receiveren til at modtage beskeder fra serveren. jeg starter den i en
# thread så det stadig er muligt at gøre andre ting imens den køre i baggrunden.
    def run_gui(self):
        print("Starting GUI")
        client_receiver = Thread(target=lambda: self.receiver())
        client_receiver.start()
        self.client_gui.mainloop()

# dette er en funktion til at sende beskeder til serveren.
    def send_message(self, message):
        client.send(message.encode(format))

# dette er recieveren som bliver startet til at modtage beskeder. når den modtager en besked indsætter den den i chat
# boksen. der er også et check som checker om beskeden er dårlig som kan betyde at der er et problem med forbindelsen
# hvor den så lukker forbindelsen.
    def receiver(self):
        while True:
            try:
                self.broadcast_message = client.recv(1024).decode(format)
                self.messages.insert(INSERT, '%s\n' % self.broadcast_message)
                self.messages.yview_pickplace("end")
            except:
                client.close()

# dette er en funktion til at vise en information om klienten og brugernavn den bliver brugt i drop down menuen.
    def info(self):
        string = "Username: {} \n running: clientGUI ".format(self.username[0])
        self.popup_message(string)

# dette er admin guien som nedarver klient guien og har så nogle andre funktioner
class AdminGui(ClientGui):
    def __init__(self, *username):
        super().__init__()
        self.username = username
        # her tilføjer jeg mere til dropdown menuen.
        self.filemenu.add_command(label="Ban", command=self.ban_user())
        self.client_gui.config(menu=self.menubar)

# her har jeg så lavet info metoden igen og overskriver den så, så den gør noget andet i adminGUIen.
    def info(self):
        string = "Username: {} \n running: adminGUI \n Current server: {}:{} \n Your IP: {} "\
            .format(self.username[0], server, port, socket.gethostbyname(socket.gethostname()))
        self.popup_message(string)

    def ban_user(self):
        #mangler
        self.send_message("!ban")

# dette starter login guien så programmet kan starte.
client = LoginGUI()