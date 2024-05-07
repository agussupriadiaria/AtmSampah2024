/* 
PROGRAM : CONVEYOR OKTOBER 2022
Part : Nema 17, tb6600, LED
Setting: 
- Arduino Uno
- Microstep 16, pulse/rev 3200
- Amps: 2 Amps
- Tambahan led: siap, proses, penuh dan auto stop jika sudah penuh.
===================
Source: 
- https://mytectutor.com/tb6600-stepper-motor-driver-with-arduino/
- https://www.youtube.com/watch?v=idVcItHfGS4&ab_channel=MYTECTUTOR
===================
Issue:
-
===================
PIN:
3 > step
2 > dir
4 > en
5 > button
6 > insensor 
===================
History:
- 1 Mei 2024 > testing lagi

*/

//STEPPER MOTOR=================
const int stepPin = 3; //5 pin buat apa ini? ===========
const int dirPin = 2; //2
const int enPin = 4; //8
//INPUT FROM RASPI===============
int buttonPin = 5; //9
int buttonCondition = 0;
//POSITION STEPPER SENSOR================
int inSensorPin = 6; //3
int inSensorCondition = 0;
//LED=============
int ledPin = 7;
int siapPin = 8;
int prosesPin = 9;
int penuhPin = 13;
int penuhIn = 10; //dari sensor infrared
int penuhKondisi = 0;

void setup() {
//STEPPER MOTOR=================
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);
//OTHERS===================
  pinMode(buttonPin,INPUT_PULLUP);//Ganti pullup, karena nggak pakai resistor
  pinMode(ledPin,OUTPUT);
  pinMode(siapPin,OUTPUT);
  pinMode(prosesPin,OUTPUT);
  pinMode(penuhPin,OUTPUT);
  pinMode(penuhIn,INPUT);
  
  pinMode(inSensorPin,INPUT);
}

//LOGIC GERAKAN LOOP/PENGULANGAN
void loop(){
  fullLed();
  inSensorCondition = digitalRead(inSensorPin);
  if(inSensorCondition == LOW){
    conveyorRun();
  }
  else{
    ccwReady();
  }
}

//LOGIC GERAKAN STEPPER MOTOR MENCARI POSISI AWAL ==============
void ccwReady(){
  digitalWrite(dirPin,HIGH); //Setting CW atau CCW
  for(int x = 0; x < 200; x++) {
  digitalWrite(stepPin,HIGH); 
  delayMicroseconds(4000); 
  digitalWrite(stepPin,LOW);
  delayMicroseconds(4000); 
  }
}
//LOGIC GERAKAN STEPPER MOTOR TERATUR ==============
void stepperMove() {
  digitalWrite(dirPin,LOW); // Enables the motor to move in a particular direction
  for(int x = 0; x < 400; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(4000);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(4000);
  }
  delay(500); //Delay perlu dipakai nggak ya?
  digitalWrite(dirPin,HIGH); //Changes the direction of rotation
  for(int x = 0; x < 400; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(4000);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(4000);
  }
}

//LOGIC PRINT STRUK ==============
void conveyorRun(){
  buttonCondition = digitalRead (buttonPin);
  if(buttonCondition == LOW){ // Ini set high atau low?
    digitalWrite(ledPin,HIGH);
    digitalWrite(siapPin,LOW);
    digitalWrite(prosesPin,HIGH);
    delay(4000);
    stepperMove();
  }
  else{
    digitalWrite(ledPin,LOW);
    digitalWrite(siapPin,HIGH);
    digitalWrite(prosesPin,LOW);
  }
}

void fullLed(){
  penuhKondisi = digitalRead(penuhIn);
  if (penuhKondisi == LOW){
    digitalWrite(penuhPin,HIGH);
  }
  else{
    digitalWrite(penuhPin,LOW);
  }
}
