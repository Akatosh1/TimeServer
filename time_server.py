import socket
import time
import sys

class TimeServer():

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('localhost', 123))
        self.server.settimeout(0)
        self.test_socket.settimeout(0)
        with open("time.txt", "rb") as f:
            self.time = int(f.readline())
        
    def take_receive(self):
        data, addr = self.server.recvfrom(1024)
        if data:
            difference = time.time() - float(data)
            self.server.sendto(bytes(time.ctime(time.time() + self.time + difference*2), encoding = "utf-8"), addr)

    def test_send(self):
        self.test_socket.sendto(bytes(str(time.time()), encoding = "utf-8"), ('localhost', 123))

    def test_receive(self):
        data, addr = self.test_socket.recvfrom(1024)
        print("Ответ сервера: " + str(data))

timeServer = TimeServer()
print("Режим работы?")
print("test - тестовый; common - в режиме сервера")
t = input()
try:
    if t == "test":
        while True:
            print("Напишите что-нибудь чтобы протестировать сервер")
            print("Или напишите change чтобы поменять врущее время")
            inpu = input()
            if inpu == "change":
                print("Новое время:")
                inp = input()
                timeServer.time = int(inp)
                with open("time.txt", "wb")as f:
                    f.write(bytes(inp, encoding = "utf-8"))
            timeServer.test_send()
            timeServer.take_receive()
            timeServer.test_receive()
    else:
        while True:
            timeServer.take_receive()
except KeyboardInterrupt:
    print("Сервер успешно завершил работу")
except Exception as e:
    print("Сервер выключается из-за ошибки")
    print(e)
finally:
    timeServer.server.close()
    timeServer.test_socket.close()
    time.sleep(1)
    sys.exit(0)
    