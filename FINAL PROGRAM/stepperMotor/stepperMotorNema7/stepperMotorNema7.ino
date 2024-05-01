/*
 * Source: https://mytectutor.com/tb6600-stepper-motor-driver-with-arduino/
 * 
*/

const int stepPin = 5; 
const int dirPin = 2; 
const int enPin = 8;
int buttonPin = 9;
int ledPin = 13;
int buttonCondition = 0;

void setup() {
  //ketika board stepper tereset, auto run sampai menyentuh sensor posisi agar posisi stepper jadi 0 kembali
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(buttonPin,INPUT);
  pinMode (ledPin,OUTPUT);
  digitalWrite(enPin,LOW);
  
}

void loop(){
  buttonCondition = digitalRead (buttonPin);
  if(buttonCondition == HIGH){
    digitalWrite(ledPin,HIGH);
    stepperMove();
  }
  else{
    digitalWrite(ledPin,LOW);
  }
}

void stepperMove() {
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  for(int x = 0; x < 2000; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(1000); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(1000); 
  }
  delay(1000); // One second delay
  digitalWrite(dirPin,LOW); //Changes the direction of rotation
  for(int x = 0; x < 800; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(1000);
  }
  delay(2000); 
}
