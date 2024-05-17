import serial
from serial.tools.list_ports import comports
import time

# 아두이노의 포트 자동 탐지
def find_arduino_port():
    ports = comports()
    for port, desc, hwid in sorted(ports):
        if 'arduino' in desc.lower():
            return port
    return None

# 아두이노와의 시리얼 통신 설정
arduino_port = find_arduino_port()
if arduino_port is None:
    print("아두이노를 찾을 수 없습니다.")
    exit()

baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # 아두이노와의 시리얼 통신이 확립될 때까지 잠시 대기

while True:
    command = input("LED를 제어할 명령을 입력하세요 (1: 켜기, 0: 끄기): ")
    ser.write(command.encode())  # 명령을 바이트 형태로 아두이노에게 전송