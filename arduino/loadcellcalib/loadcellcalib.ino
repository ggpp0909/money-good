#include <Arduino.h>
#include <HX711.h>

const int loadCellPinDT = 5; //HX711의 DT핀과 연결된 아두이노 핀 번호
const int loacCellPinSCK = 6; //HX711의 SCK핀과 연결된 아두이노 핀 번호

float scaleDivide = 372000; //제조사, 제품 마다 차이 발생 (20kg 기준)

HX711 scale;

void setup() {

  Serial.begin(9600); //Baud Rate 설정

  scale.begin(loadCellPinDT, loacCellPinSCK); //연결

  /*
  1. 아무 것도 올려 놓지 않아야 함
  2. 무게를 알고 있는 물건을 놓아야 함
  3. "+" 입력 후 엔터 키 -> scaleDivide 값 100 씩 증가 시킴
  4. "-" 입력 후 엔터 키 -> scaleDivide 값 100 씩 감소 시킴
  */

  scale.set_scale(); //기본 스케일 값 설정
  scale.tare(); //처음 시작시 0 점 잡기
}

void loop() {
  scale.set_scale(scaleDivide); //변경되는 scaleDivide 을 적용 함

  Serial.print("Reading: ");
  Serial.print(scale.get_units(), 3);
  Serial.println(" kg"); //단위 표시, g, kg, lb 등
  Serial.print(" scaleDivide: ");
  Serial.print(scaleDivide);
  Serial.println();
  
  if(Serial.available())
  {
    char temp = Serial.read(); //입력된 값

    if(temp == '+') {
      scaleDivide += 1000;
    } 
    else if(temp == '-')
    {
      scaleDivide -= 1000;
    }
  }

  delay(300); //1초 delay (1초 마다 반복)
}

