import serial
import time
import serial.tools.list_ports

# Function to find the Arduino port automatically
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None

# Function to send a command to the Arduino and wait for a response
def send_command(ser, command, delay):
    # ser.write(command.encode())
    time.sleep(delay)
    if command == 'O':
        weight = 990
        # weight = ser.readline().strip().decode()
        print(f"Measured weight: {weight} grams")
        return weight

# Main script
# arduino_port = find_arduino_port()
# if arduino_port is None:
#     print("Could not find an Arduino connected to the computer.")
#     exit()

# ser = serial.Serial(arduino_port, 9600)
# time.sleep(2)  # Wait for the serial connection to establish

# try:
#     # Step 1: Open the door and measure weight
#     weight = send_command(ser, 'O', 3)
    
#     # Step 2: Start the 220V AC motor
#     send_command(ser, 'M', 5)
    
#     # Step 3: Close the door
#     send_command(ser, 'C', 3)
# finally:
#     ser.close()
