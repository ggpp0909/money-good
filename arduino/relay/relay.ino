int RELAY1 = 7;


void setup() {
  Serial.begin(9600);// put your setup code here, to run once:
  pinMode(RELAY1,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'c') 
    {
      digitalWrite(RELAY1,HIGH);
      Serial.println("Motor Off");
    } 
    else if (command == 'o') 
    {
      digitalWrite(RELAY1,LOW);
      Serial.println("Motor On");
    }
  }
}
