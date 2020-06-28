import sys
import glob
import serial
from serial.tools import list_ports
def serial_ports():
    return [(port.device,port.manufacturer) for port in list_ports.comports(include_links=False)]


if __name__ == '__main__':
    print(serial_ports())