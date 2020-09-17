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
                        'Server=DESKTOP-K2BR3A1\SQLEXPRESS;'
                        'Database=Chatapp;'
                        'Trusted_Connection=yes;')
cursor = dbconn.cursor()
print("Connected...")


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
    string = 'SELECT * FROM Users WHERE Username = \'%s\'' % (username)
    test = database_read(string)
    checkUsername = test.fetchall()
    print(checkUsername)
    if not checkUsername:
        return True
    else:
        return False


check_username("tau49")


class UserFactory:
    def create_user(self, name, password):
        print("Test")


while True:
    c, addr = s.accept()
    userinfo = pickle.loads(c.recv(1024))

    c.send('Username'.encode("utf-8"))
    c.close()
