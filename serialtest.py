import serial
import serial.tools.list_ports
import time

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if 'Arduino' in desc or 'CH340' in desc:
            return port
    return None

# Find the Arduino port
arduino_port = find_arduino_port()
if arduino_port is None:
    print("Arduino not found. Please check the connection.")
    exit()

# Establish serial connection
ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

def read_serial():
    if ser.in_waiting > 0:
        return ser.readline().decode().strip()
    else:
        return None

def send_command(command):
    try:
        ser.write(command.encode())
        time.sleep(0.1)
        response = read_serial()
        return response
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        return ""

def open_door():
    print("Opening the door...")
    response = send_command('O')
    if response:
        print(f"Response from Arduino: {response}")
    else:
        print("No response from Arduino.")

def close_door():
    print("Closing the door...")
    response = send_command('C')
    if response:
        print(f"Response from Arduino: {response}")
    else:
        print("No response from Arduino.")

def measure_weight():
    print("Measuring weight...")
    response = send_command('R')
    if response:
        print(f"Weight from Arduino: {response} g")
    else:
        print("No response from Arduino.")

def stop_measuring_weight():
    print("Stopping weight measurement...")
    response = send_command('D')
    if response:
        print(f"Response from Arduino: {response}")
    else:
        print("No response from Arduino.")

def operate_motor():
    print("Starting 220V AC motor...")
    response = send_command('M')
    if response:
        print(f"Response from Arduino: {response}")
    else:
        print("No response from Arduino.")

if __name__ == "__main__":
    try:
        while True:
            # Read and print any incoming data from Arduino
            data = read_serial()
            if data:
                print(f"Arduino: {data}")

            command = input("Enter command (O: Open door, C: Close door, R: Measure weight, D: Stop measuring weight, M: Operate motor, Q: Quit): ").strip().upper()
            if command == 'O':
                open_door()
            elif command == 'C':
                close_door()
            elif command == 'R':
                measure_weight()
            elif command == 'D':
                stop_measuring_weight()
            elif command == 'M':
                operate_motor()
            elif command == 'Q':
                print("Exiting...")
                break
            else:
                print("Invalid command. Please try again.")
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt. Exiting...")
    finally:
        if ser.is_open:
            ser.close()
