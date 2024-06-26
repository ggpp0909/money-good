#include "HX711.h"

const int IN1 = 3; //OUT1 Green  
const int IN2 = 4; //OUT2 Yellow
const int IN3 = 13; //OUT3 
const int IN4 = 12; //
const int ENA = 9;   
const int ENB = 10;  
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 6;
const int relayPinM = 7;
const int relayPinS = 8;
unsigned long SMotorTime = 10000; //10 sec
unsigned long BMotorTime = 60000; //60 sec

bool isDoorOpened = false;
bool isDoorClosed = false;
bool isWeightMeasured = false;


HX711 scale;
float scale_factor = 372000;  //Calibrated value
float weight;

void setup() 
{
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(ENA,OUTPUT);    
  pinMode(ENB,OUTPUT);
  pinMode(relayPinM, OUTPUT);
  pinMode(relayPinS, OUTPUT);
  digitalWrite(relayPinM,HIGH);  // EnableA를 점퍼 핀 연결한 환경과 동일하게
  digitalWrite(relayPinS,HIGH);  // EnableA를 점퍼 핀 연결한 환경과 동일하게
  digitalWrite(ENA,HIGH);  // EnableA를 점퍼 핀 연결한 환경과 동일하게
  digitalWrite(ENB,HIGH);  //EnableB를 점퍼 핀 연결한 환경과 동일하게
  analogWrite(ENA, 250);    //0~255 값으로 속도를 조절하고자 할 때
  analogWrite(ENB, 250);    // 0~255 값으로 속도를 조절하고자 할 때
  
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale();
  scale.tare();

  Serial.begin(9600);
}

void stop_door()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
  
  // Serial.println("Stop");  
}

void move_forward()
{
  int fwdcnt = 0;
  while(isDoorOpened)
  {
    if(fwdcnt < 251)
    {
      digitalWrite(IN1,LOW);
      digitalWrite(IN2,HIGH);
      digitalWrite(IN3,HIGH);
      digitalWrite(IN4,LOW);
      delay(3);
        
      digitalWrite(IN1,LOW);
      digitalWrite(IN2,HIGH);
      digitalWrite(IN3,LOW);
      digitalWrite(IN4,HIGH);
      delay(3);
          
      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,LOW);
      digitalWrite(IN3,LOW);
      digitalWrite(IN4,HIGH);
      delay(3);
          
      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,LOW);
      digitalWrite(IN3,HIGH);
      digitalWrite(IN4,LOW);
      delay(3); 
      fwdcnt++;

    }
    else
    {
      isDoorOpened = false;
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      // Serial.println("Forward cnt:");
      // Serial.println(fwdcnt);
      fwdcnt = 0;

    }

    if (Serial.available()) 
    {
      char command = Serial.read();
      if (command == 'b') 
      {
        isDoorOpened = false;
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        // Serial.println("Forward cnt:");
        // Serial.println(fwdcnt);
        fwdcnt = 0;
      }
    }
  }
}

void move_backward()
{
  int bwdcnt = 0;
  while(isDoorClosed)
  {
    if(bwdcnt < 251)
    {
      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,LOW);
      digitalWrite(IN3,HIGH);
      digitalWrite(IN4,LOW);
      delay(3);

      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,LOW);
      digitalWrite(IN3,LOW);
      digitalWrite(IN4,HIGH);
      delay(3);

      digitalWrite(IN1,LOW);
      digitalWrite(IN2,HIGH);
      digitalWrite(IN3,LOW);
      digitalWrite(IN4,HIGH);
      delay(3);

      digitalWrite(IN1,LOW);
      digitalWrite(IN2,HIGH);
      digitalWrite(IN3,HIGH);
      digitalWrite(IN4,LOW);
      delay(3);
      bwdcnt++;
    }
    else
    {
      isDoorClosed = false;
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      // Serial.println("Backward count:");
      // Serial.println(bwdcnt);
      bwdcnt = 0;

    }

    if (Serial.available())
    {
      char command = Serial.read();
      if (command == 'b') 
      {
        isDoorClosed = false;
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        // Serial.println("Backward count:");
        // Serial.println(bwdcnt);
        bwdcnt = 0;
      }
    }
  }
}

void measures_weight()
{
  while(isWeightMeasured)
  {
    weight = scale.get_units(3);
    scale.set_scale(scale_factor);
    // Serial.print("Sending weight info: ");
    weight = weight*1000;
    Serial.print(weight);
    delay(100);

    if (Serial.available())
    {
      break;
    }
  }
}

void loop() 
{
  if (Serial.available()) 
  {
    char command = Serial.read();
    
    if(command == 'O') 
    {  
      // Open door
      isDoorOpened = true;
      // Serial.println("Open the door");
      move_forward();
      // Measure weight
      isWeightMeasured = true;
      measures_weight();
      
    }
    else if (command == 'C') 
    {  
      // Close door
      isDoorClosed = true;
      move_backward();

      isWeightMeasured = true;
      measures_weight();

      
    }
    else if (command == 'M') 
    {  // Start Small Motor
      isWeightMeasured = false;
      digitalWrite(relayPinM, LOW);
      delay(SMotorTime); // Adjust based on operation time
      digitalWrite(relayPinM, HIGH);
    }
    else if (command == 'S') 
    {  // Start Big Motor 
      float response  = 1; 
      Serial.print(response);
      isWeightMeasured = false;
      digitalWrite(relayPinS, LOW);
      delay(BMotorTime); // Adjust based on operation time
      digitalWrite(relayPinS, HIGH);
    }
    else if (command == 'R') 
    {  
      // Measure weight
      isWeightMeasured = true;
      measures_weight();
    }
    else if (command == 'D') 
    {
      isWeightMeasured = false;  
    }
    
  }
}
