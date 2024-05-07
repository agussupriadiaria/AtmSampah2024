/*
Source: https://mytectutor.com/tb6600-stepper-motor-driver-with-arduino/

Pin yang nempel di Uno:
2 Dir + x
3 Pull + 
4 Ena + x
5 Input dari relay x
6 IR sensor stepper position

8 LED siap x
9 LED proses x

*/

const int stepPin = 3; // PullPin --- done
const int dirPin = 2; //--- bener
const int enPin = 4; //--- bener
int buttonPin = 5; // dari relay raspberry--- done
int ledPinSiap = 8; //---done
int ledPinProses = 9; // --- done

int buttonCondition = 0;

void setup() {
  //ketika board stepper tereset, auto run sampai menyentuh sensor posisi agar posisi stepper jadi 0 kembali
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(buttonPin,INPUT);
  pinMode (ledPinSiap,OUTPUT);
  pinMode (ledPinProses,OUTPUT);
  digitalWrite(enPin,LOW);
}

void loop(){
  buttonCondition = digitalRead (buttonPin);
  if(buttonCondition == HIGH){
    digitalWrite(ledPinProses,HIGH);
    digitalWrite(ledPinSiap,LOW);
    stepperMove();
  }
  else{
    digitalWrite(ledPinProses,LOW);
    digitalWrite(ledPinSiap,HIGH);
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
