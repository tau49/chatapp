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


def commandhandler(user_command, connection):
    commandlst = user_command.split(' ')
    command_user = get_username(connection)
    command = commandlst[0]
    username = commandlst[1]

    if is_admin(command_user):
        if command == "!ban":
            reason = commandlst[2]
            if len(commandlst) == 3:
                return command_ban_user(username, reason)
            elif len(commandlst) == 4:
                min_banned = commandlst[3]
                return command_ban_user(username, reason, min_banned)
        elif command == "!unban":
            return command_unban_user(username)
        elif command == "!admin":
            return command_make_admin(username)
        elif command == "!create":
            password = commandlst[2]
            return command_create_user(username, password)
        elif command == "!delete":
            return command_delete_user(username)
        elif command == "!extend":
            time = commandlst[2]
            return command_extend_ban(username, time)
        elif command == "!read":
            return command_read_user(username)
    else:
        return False


def command_ban_user(username, reason, minutes_banned=None):
    if check_username(username):
        if minutes_banned is None:
            minutes_banned = 20000
        userid = get_id(username)
        sql = 'INSERT INTO Banned_Users(UserID, Ban_Date, Ban_Reason, Banned_until) ' \
              'VALUES({}, GETDATE(), \'{}\', {})'.format(userid, reason, minutes_banned)
        database_write(sql)
        return True
    else:
        return False


def command_unban_user(username):
    if check_username(username):
        user_id = get_id(username)
        sqlquary = database_read('SELECT * FROM Users WHERE Username = \'%s\'' % user_id)
        check_banned = sqlquary.fetchall()
        if not check_banned:
            return False
        else:
            database_write('DELETE FROM Banned_Users where UserID = \'%s\'' % user_id)
            return True


def command_create_user(username, user_password):
    create_user(username, user_password)
    return True


def command_delete_user(username):
    database_write('DELETE FROM Users where UserID = \'%s\'' % get_id(username))
    return True


def command_make_admin(username):
    if check_username(username):
        sqlquary = 'UPDATE Users SET Is_admin = 1 WHERE UserID = %d' % (get_id(username))
        database_write(sqlquary)
        return True
    else:
        return False


def command_extend_ban(username, minutes):
    sqlquary = 'UPDATE Banned_Users SET Banned_until = {} WHERE UserID = {}'.format(minutes, get_id(username))
    database_write(sqlquary)
    return True


def command_read_user(username):
    result = database_read('SELECT Username, Password FROM Users where Username = \'{}\''.format(username)).fetchone()
    if result == "unittest":
        return True


def create_user(user_username, user_password):
    database_write('INSERT INTO Users(Username, Password) VALUES (\'%s\',\'%s\');' % (user_username, user_password))
    return True


def login(login_username, login_password):
    if check_username(login_username):
        sqlcommand = 'EXEC check_login @user_username = \'%s\', @user_password = \'%s\'' \
                     % (login_username, login_password)
        cursor = database_read(sqlcommand)
        result = cursor.fetchone()
        if result[0] == 1:
            return True
        elif result[0] == 0:
            return False
        else:
            return False
    else:
        return False


def database_read(sql_command):
    cursor.execute(sql_command)
    return cursor


def database_write(sql_command):
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


def is_admin(username):
    sqlquary = database_read('SELECT Is_admin FROM Users WHERE Username = \'%s\'' % (username))
    isadmin = sqlquary.fetchone()
    if isadmin[0] == 1:
        return True
    else:
        return False


def get_username(connection):
    username = client_names[client_list.index(connection)]
    return username


def get_id(username):
    sqlquary = database_read('SELECT UserID FROM Users WHERE Username = \'%s\'' % (username))
    user_id = sqlquary.fetchone()
    return user_id[0]


def stop_connection(client_connection):
    if client_connection in client_list:
        client_list.remove(connection)


def client_thread(client_connection):
    while True:
        try:
            message = client_connection.recv(1024).decode(format)
            if message:
                if message[0] == "!":
                    if message == '!exit':
                        stop_connection(client_connection)
                    else:
                        result = commandhandler(message, client_connection)
                        client_connection.send(str(result).encode(format))
                else:
                    broadcast(message, client_connection)
            else:
                stop_connection(client_connection)
                break
        except:
            continue


def broadcast(message, conn):
    for client in client_list:
        if not client == conn:
            client.send(message.encode(format))


s.listen(10)

while True:
    connection, address = s.accept()
    userinfo = pickle.loads(connection.recv(1024))
    username = userinfo[0]
    password = userinfo[1]
    command = userinfo[2]
    if command == "register":
        if check_username(username):
            connection.send('Username is already in use'.encode("utf-8"))
        else:
            connection.send('Welcome'.encode("utf-8"))
            create_user(username, password)
            client_list.append(connection)
            client_names.append(username)
            break
    elif command == "login":
        if login(username, password):
            client_list.append(connection)
            client_names.append(username)
            connection.send('Login success'.encode("utf-8"))
            thread = Thread(target=client_thread, args=(connection,))
            thread.start()
        else:
            connection.send('Login failed'.encode("utf-8"))
