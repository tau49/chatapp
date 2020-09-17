import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = socket.gethostbyname(socket.gethostname())
port = 52245
s.bind(('', port))
clients, names = [], []
s.listen(10)

while True:
    c, addr= s.accept()
    c.send('Test'.encode("utf-8"))
    c.close()
