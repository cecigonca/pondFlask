from pydobot import Dobot
from serial.tools import list_ports

class TheRobot:
    def __init__(self):
        self.port = self.scan_ports() 
        if self.port:
            self.robot = Dobot(port=self.port, verbose=False)
            self.robot.speed(200, 200)
        else:
            self.robot = None
            raise Exception("No robot found!")

    def scan_ports(self):
        available_ports = list_ports.comports()
        for port in available_ports:
            try:
                test_robot = Dobot(port=port.device, verbose=False)
                test_robot.close() 
                print(f"Robot found on: {port.device}")
                return port.device  
            except Exception as e:
                print(f"No robot found on: {port.device}. Error: {e}")
        return None

    def turn_on(self):
        if self.robot:
            self.robot.suck(True)

    def turn_off(self):
        if self.robot:
            self.robot.suck(False)

    def current(self):
        if self.robot:
            return self.robot.pose()
        return None

    def mover(self, x, y, z, r, wait=True):
        if self.robot:
            self.robot.move_to(x, y, z, r, wait=wait)

    def home(self):
        if self.robot:
            x, y, z, r = 100, 0, 0, 0
            self.robot.move_to(x, y, z, r, wait=True)