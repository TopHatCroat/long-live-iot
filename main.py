import network
import machine
import time
import usocket as socket
import ujson as json

class Flashlight:
    def __init__(self):
        self.led = machine.Pin(2, machine.Pin.OUT)

    def toggle(self):
        self.led.value(not self.led.value())
    
    def on(self):
        self.led.low()

    def off(self):
        self.led.high()


    def blink(self, len, count):
        for x in range(0, count * 2):
            time.sleep_ms(len)
            self.toggle()

class AP:
    def __init__(self, ssid = "Mini Vaj-Faj", passwd = "12345678"):
        self.ap = network.WLAN(network.AP_IF)
        self.ssid = ssid
        self.passwd = passwd

    def make(self):
        self.ap.active(True)
        self.ap.config(essid = self.ssid, password = self.passwd)
        self.ap.config()

    def stop(self):
        self.ap.active(False)

    def isActive(self):
        return self.ap.active()


class Internet:
    def __init__(self, name = "8========D~", password = "nostiposran"):
        self.wlan = network.WLAN(network.STA_IF)
        self.name = name
        self.password = password

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.name, self.password)
    
    def isConn(self):
        return self.wlan.isconnected()

    def getIp(self):
        return self.wlan.ifconfig()[0]


class Server:
    WRAPPER = """\
        HTTP/1.0 200 OK

        {}
        """

    def __init__(self, addr = "0.0.0.0", port = 8080):
        self.ai = socket.getaddrinfo(addr, port)
        self.addr = self.ai[0][4]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        
    def listen(self, count = 1):
        self.sock.listen(count)
        led = Flashlight()
        while True:
            res = self.sock.accept()
            print("Connection: ", res)
            req = res[0].recv(4096)
            print(req)
            led.toggle()
            # res[0].send(bytes(self.WRAPPER.format("I am alive"), "ascii"))
            res[0].send(json.dumps(["lol","derp"]))
            res[0].close()
            parts = req.decode('ascii')
            print(parts)
            parts = parts.split(' ')
            print(parts)
            if parts[1] == '/exit':
                break
            if parts[1] == '/party':
                led.blink(200, 10)

inter = Internet()
serv = Server()
serv.listen()