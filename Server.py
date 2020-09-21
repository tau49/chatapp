import socket
import pickle
import pyodbc

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = socket.gethostbyname(socket.gethostname())
port = 52245
s.bind(('', port))
clients, names = [], []
s.listen(10)

print("connecting to database...")
dbconn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DRL-PC1608;'
                        'Database=Chatapp;'
                        'Trusted_Connection=yes;')
cursor = dbconn.cursor()
print("Connected...")


class user:
    def __init__(self, user_username, user_password):
        self.username = user_username
        self.password = user_password
    def create_user(self):
        database_write('INSERT INTO Users(Username, Password) VALUES (\'%s\',\'%s\');' % (self.username, self.password))

    def hash_password(self):
        print("test")

    def check_login(self):
        print("")
    


def database_read(sql_command):
    print(sql_command)
    cursor.execute(sql_command)
    return cursor


def database_write(sql_command):
    cursor.execute(sql_command)
    cursor.execute(sql_command)
    dbconn.commit()
    return cursor


def check_username(username):
    test = database_read('SELECT * FROM Users WHERE Username = \'%s\'' % (username))
    checkUsername = test.fetchall()
    print(checkUsername)
    if not checkUsername:
        return False
    else:
        return True



while True:
    c, addr = s.accept()
    userinfo = pickle.loads(c.recv(1024))
    username = userinfo[0]
    password = userinfo[1]
    if check_username(username):
        print("Username is already in use")
        c.send('Username is already in use'.encode("utf-8"))
    else:
        create_user(username, password)
    c.close()