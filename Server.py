import socket
import pickle
from threading import Thread

import pyodbc

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = socket.gethostbyname(socket.gethostname())
port = 52245
ADDRESS = (server_address, port)
print(server_address)
s.bind(ADDRESS)
client_list = []
client_names = []
format = "utf-8"

print("connecting to database...")
dbconn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-K2BR3A1\SQLEXPRESS;'
                        # 'Server=DRL-PC1608;'
                        'Database=Chatapp;'
                        'Trusted_Connection=yes;')
cursor = dbconn.cursor()
print("Connected...")


def create_user(user_username, user_password):
    database_write('INSERT INTO Users(Username, Password) VALUES (\'%s\',\'%s\');' % (user_username, user_password))


def hash_password():
    print("test")


def login(login_username, login_password):
    if check_username(login_username):
        sqlcommand = 'EXEC check_login @user_username = \'%s\', @user_password = \'%s\'' \
                     % (login_username, login_password)
        cursor = database_read(sqlcommand)
        result = cursor.fetchone()
        print(result[0])
        if result[0] == 1:
            print("true")
            return True
        elif result[0] == 0:
            print("false")
            return False
        else:
            print("false2")
            return False
    else:
        return False


def database_read(sql_command):
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
    if not check_username:
        return False
    else:
        return True


# def check_command()

def stop_connection(client_connection):
    if client_connection in client_list:
        client_list.remove(connection)


def client_thread(client_connection):
    while True:
        try:
            message = client_connection.recv(1024).decode(format)
            print(message)
            if message:
                if message[0] == "!":
                    if message == '!exit':
                        stop_connection(client_connection)
                    else:
                        print("check command")
                else:
                    print("i get here")
                    broadcast(message, client_connection)
            else:
                print("tes4564654t")
                stop_connection(client_connection)
                break
        except:
            continue


def broadcast(message, conn):
    for client in client_list:
        print(conn)
        print(client)
        if not client == conn:
            client.send(message.encode(format))
        print("i get here")


s.listen(10)

while True:
    print("oi")
    connection, address = s.accept()
    userinfo = pickle.loads(connection.recv(1024))
    username = userinfo[0]
    password = userinfo[1]
    command = userinfo[2]
    if command == "register":
        if check_username(username):
            print("Username is already in use")
            connection.send('Username is already in use'.encode("utf-8"))
        else:
            connection.send('Welcome'.encode("utf-8"))
            create_user(username, password)
            client_list.append(connection)
            client_names.append(username)
            break
    else:
        if login(username, password):
            client_list.append(connection)
            client_names.append(username)
            connection.send('Login success'.encode("utf-8"))
            print("test")
            thread = Thread(target=client_thread, args=(connection,))
            print("test")
            thread.start()
            print("test")
        else:
            connection.send('Login failed'.encode("utf-8"))
