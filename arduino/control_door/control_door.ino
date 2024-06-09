#include <Stepper.h>

// Define number of steps per revolution
const int stepsPerRevolution = 200;  // Change this based on your motor's specifications

// Initialize stepper library on pins 8 through 11
Stepper myStepper(stepsPerRevolution, 3, 4, 12, 13);

void setup() {
  // Set speed of the motor
  myStepper.setSpeed(60);  // Adjust as necessary

  // Initialize serial communication
  Serial.begin(9600);
  Serial.println("Stepper Motor Control Initialized");
}

void loop() {
  // Check for serial input
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'o') {
      openDoor();
    } else if (command == 'c') {
      closeDoor();
    }
  }
}

// Function to open the door
void openDoor() {
  Serial.println("Opening door...");
  myStepper.step(stepsPerRevolution);  // Adjust number of steps based on your setup
}

// Function to close the door
void closeDoor() {
  Serial.println("Closing door...");
  myStepper.step(-stepsPerRevolution);  // Adjust number of steps based on your setup
}
