int RELAY1 = 7;
// int RELAY1 = 8;


void setup() {
  Serial.begin(9600);// put your setup code here, to run once:
  pinMode(RELAY1,OUTPUT);
  digitalWrite(RELAY1,HIGH);  // EnableA를 점퍼 핀 연결한 환경과 동일하게

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
