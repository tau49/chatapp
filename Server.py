import socket
import pickle
import pyodbc

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = socket.gethostbyname(socket.gethostname())
port = 52245
s.bind(('', port))
client_list = []
client_names = []
s.listen(10)

print("connecting to database...")
dbconn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-K2BR3A1\SQLEXPRESS;'
                        'Database=Chatapp;'
                        'Trusted_Connection=yes;')
cursor = dbconn.cursor()
print("Connected...")


def create_user(user_username, user_password):
    database_write('INSERT INTO Users(Username, Password) VALUES (\'%s\',\'%s\');' % (user_username, user_password))


def hash_password():
    print("test")


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
    check_username = test.fetchall()
    print(check_username)
    if not check_username:
        return False
    else:
        return True

def client_thread(client_connection, client_address):
    


while True:
    connection, address = s.accept()
    if connection:
        while True:
            userinfo = pickle.loads(connection.recv(1024))
            username = userinfo[0]
            password = userinfo[1]
            if check_username(username):
                print("Username is already in use")
                connection.send('Username is already in use'.encode("utf-8"))
            else:
                create_user(username, password)
                client_list.append(connection)
                client_names.append(username)
                break
