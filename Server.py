import socket
import pickle
from threading import Thread
import pyodbc

# initialisere serveren
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = socket.gethostbyname(socket.gethostname())
port = 52245
ADDRESS = (server_address, port)
print(server_address)
s.bind(ADDRESS)
client_list = []
client_names = []
format = "utf-8"

# forbinder til sql serveren og logger forbindelsen ind i dbconn objektet.
print("connecting to database...")
dbconn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-K2BR3A1\SQLEXPRESS;'
                        # 'Server=DRL-PC1608;'
                        'Database=Chatapp;'
                        'Trusted_Connection=yes;')
cursor = dbconn.cursor()
print("Connected...")


# dette er command handleren, som tager en command fra klienten som starter ud som en string og så splitter den op så
# den kan håndtere den. efter den er blevet splittet så finder den så ud af om brugeren er er admin ved at spørger
# sql serveren. hvorefter den finder ud af hvad brugeren vil og så kalder den metode som ønskes.
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


# command som banner en user ved at skrive det til sql serveren. Denne command har jeg lavet overloading da den kan tage
# enten 2 eller 3 inputs f.eks. hvis den får 2 så sætter den en standard værdi af 20000.

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


# command til at unbanne en user.
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


# laver en bruger på sql serveren.
def command_create_user(username, user_password):
    create_user(username, user_password)
    return True


# sletter en bruger på sql serveren.
def command_delete_user(username):
    database_write('DELETE FROM Users where UserID = \'%s\'' % get_id(username))
    return True


# laver en bruger til admin.
def command_make_admin(username):
    if check_username(username):
        sqlquary = 'UPDATE Users SET Is_admin = 1 WHERE UserID = %d' % (get_id(username))
        database_write(sqlquary)
        return True
    else:
        return False


# ændre hvor langt tid en bruger er banned.
def command_extend_ban(username, minutes):
    sqlquary = 'UPDATE Banned_Users SET Banned_until = {} WHERE UserID = {}'.format(minutes, get_id(username))
    database_write(sqlquary)
    return True


# command til unit test som læser et brugernavn og så tjekker om det er lig med unittest og så retunere den så
# true eller false.
def command_read_user(username):
    result = database_read('SELECT Username, Password FROM Users where Username = \'{}\''.format(username)).fetchone()
    if result == "unittest":
        return True


# metoden til at lave en bruger denne bliver kaldt i commands og når en server opretter en bruger for klienten.
def create_user(user_username, user_password):
    database_write('INSERT INTO Users(Username, Password) VALUES (\'%s\',\'%s\');' % (user_username, user_password))
    return True


# dette er login metoden som tjekker om brugernavn og password eksistere i sql serveren. retunere så resulatet til serveren. den bruger en stored procedure på sql serveren til at checke.
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


# metoede til at læse fra databasen returner resultatet fra sql statementen.
def database_read(sql_command):
    cursor.execute(sql_command)
    return cursor


# metode til at skrive til databasen grunden til at der er både en læse og skrive er at skrive har brug for en
# ekstra commit før den skriver.
def database_write(sql_command):
    cursor.execute(sql_command)
    dbconn.commit()
    return cursor


# metode til at tjekke om usernamet eksistere bliver bl.a. brugt i commands for at tjekke om der er en bruger
# som commanden kan bruges på.
def check_username(username):
    test = database_read('SELECT * FROM Users WHERE Username = \'%s\'' % (username))
    check_username = test.fetchall()
    if not check_username:
        return False
    else:
        return True


# checker om brugeren er admin og retunere true/false
def is_admin(username):
    sqlquary = database_read('SELECT Is_admin FROM Users WHERE Username = \'%s\'' % (username))
    isadmin = sqlquary.fetchone()
    if isadmin[0] == 1:
        return True
    else:
        return False


# metode til at finde usernamet ud fra en connection.
def get_username(connection):
    username = client_names[client_list.index(connection)]
    return username


# metode til at finde userID ud fra username, som den spørger sql serveren efter.
def get_id(username):
    sqlquary = database_read('SELECT UserID FROM Users WHERE Username = \'%s\'' % (username))
    user_id = sqlquary.fetchone()
    return user_id[0]


# metode til at stoppe en forbindelse og fjerne brugeren fra bruger listen.
def stop_connection(client_connection):
    if client_connection in client_list:
        client_list.remove(connection)


# klient threaden som bliver startet når en bruger er authenticated det er den som modtager beskeder fra brugeren
# og så finder ud af om det er en command eller om det er en normal besked. hvis det er en command så kalder
# den commandhandleren. hvis det er en normal besked kalder den broadcast metoden
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

# broadcast metoden som sender beskeden ud til alle klienter undtaget den som sendte beskeden.
def broadcast(message, conn):
    for client in client_list:
        if not client == conn:
            client.send(message.encode(format))

# begynder at lytte efter forbindelser.
s.listen(10)

#det her er hovedelen af serveren som er et loop som kører hele tiden indtil serveren stoppes.
# Den modtager en forbindelse og så finder den så ud af om klieten vil registrere en bruger eller logge ind.
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
