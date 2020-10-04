import unittest
import pickle
import socket

port = 52245
server = "192.168.87.104"
address = (server, port)
format = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)
client.send(pickle.dumps(["1", "1", "login"]))
message = client.recv(1024).decode(format)
username = "unittest"
password = "unittest"

class UnitTest(unittest.TestCase):
    def test_login(self):
        self.assertEqual(message, 'Login success')

    def test_create_user(self):
        message = '!create {} {}'.format(username, password)
        client.send(message.encode(format))
        result = client.recv(1024).decode(format)
        self.assertEqual(bool(result), True)

    def test_commands(self):
        message = '!ban tau49 unittest 200'
        client.send(message.encode(format))
        result = client.recv(1024).decode(format)
        self.assertEqual(bool(result), True)
        message = '!unban tau49 unittest 200'
        client.send(message.encode(format))

    def test_read_user(self):
        message = '!read {}'.format(username)
        client.send(message.encode(format))
        result = client.recv(1024).decode(format)
        self.assertEqual(bool(result), True)

    def test_delete_user(self):
        message = '!delete {}'.format(username)
        client.send(message.encode(format))
        result = client.recv(1024).decode(format)
        self.assertEqual(bool(result), True)

if __name__ == '__main__':
    unittest.main()