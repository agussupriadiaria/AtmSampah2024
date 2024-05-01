/*
READ BARCODE SEND TO SERIAL
 
BOARD MEGA 2560
Task: Read barcode and send it to serial communication
Item to connect: Barcode reader & Raspy

PINS:
ARDUINO MEGA <> RASPBERRY PI



Testing: 30 April 2024

 */

#include <Wire.h>
#include <usbhid.h>
#include <usbhub.h>
#include <hiduniversal.h>
#include <SPI.h>

int mark; int aa; int bb; int cc; int dd; int ee; int ff; int gg; int hh;
int ii; int jj; int kk; int ll; int mm; int nn;

class MyParser : public HIDReportParser {
  public: 
    MyParser();
    void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf);
};

MyParser::MyParser() { 
  }

USB          Usb;
USBHub       Hub(&Usb);
HIDUniversal Hid(&Usb);
MyParser     Parser;


void setup() {  
  Serial.begin(115200);
  
  if (Usb.Init() == -1)
  Serial.println("OSC did not start.");
  delay( 200 );
  Hid.SetReportParser(0, &Parser);
}


void loop() {
Usb.Task();
}


void MyParser::Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf) {
  // If error, return
  // I don't know why it starts on 2, I just following the example
  if (buf[2] == 1) return;

  // If empty, return
  // I check on 2 because the previous if check on 2 too
  if (buf[2] == 0) return;

  // Like above, WHY it starts on 2 ?
  // What is the purpose of bit in 0 and 1 ?
  for(uint8_t i = 2; i < 3; i++){
//    Serial.print(buf[i]);
//    Serial.print(" ");

if(mark == 0){
  if(buf[2] == 30){
    aa = 1;
    }
  if(buf[2] == 31){
    aa = 2;
    }
  if(buf[2] == 32){
    aa = 3;
    }
  if(buf[2] == 33){
    aa = 4;
    }
 if(buf[2] == 34){
    aa = 5;
    }
  if(buf[2] == 35){
    aa = 6;
    }
 if(buf[2] == 36){
    aa = 7;
    }
  if(buf[2] == 37){
    aa = 8;
    }
  if(buf[2] == 38){
    aa = 9;
    }
  if(buf[2] == 39){
    aa = 0;
    }
  if(buf[2] == 40){
    }
  }


if(mark == 1){
  if(buf[2] == 30){
    bb = 1;
    }
  if(buf[2] == 31){
    bb = 2;
    }
  if(buf[2] == 32){
    bb = 3;
    }
  if(buf[2] == 33){
    bb = 4;
    }
 if(buf[2] == 34){
    bb = 5;
    }
  if(buf[2] == 35){
    bb = 6;
    }
 if(buf[2] == 36){
    bb = 7;
    }
  if(buf[2] == 37){
    bb = 8;
    }
  if(buf[2] == 38){
    bb = 9;
    }
  if(buf[2] == 39){
    bb = 0;
    }
  if(buf[2] == 40){
    }
  }


if(mark == 2){
  if(buf[2] == 30){
    cc = 1;
    }
  if(buf[2] == 31){
    cc = 2;
    }
  if(buf[2] == 32){
    cc = 3;
    }
  if(buf[2] == 33){
    cc = 4;
    }
 if(buf[2] == 34){
    cc = 5;
    }
  if(buf[2] == 35){
    cc = 6;
    }
 if(buf[2] == 36){
    cc = 7;
    }
  if(buf[2] == 37){
    cc = 8;
    }
  if(buf[2] == 38){
    cc = 9;
    }
  if(buf[2] == 39){
    cc = 0;
    }
  if(buf[2] == 40){
    }
  }


if(mark == 3){
  if(buf[2] == 30){
    dd = 1;
    }
  if(buf[2] == 31){
    dd = 2;
    }
  if(buf[2] == 32){
    dd = 3;
    }
  if(buf[2] == 33){
    dd = 4;
    }
 if(buf[2] == 34){
    dd = 5;
    }
  if(buf[2] == 35){
    dd = 6;
    }
 if(buf[2] == 36){
    dd = 7;
    }
  if(buf[2] == 37){
    dd = 8;
    }
  if(buf[2] == 38){
    dd = 9;
    }
  if(buf[2] == 39){
    dd = 0;
    }
  if(buf[2] == 40){
    }
  }


if(mark == 4){
  if(buf[2] == 30){
    ee = 1;
    }
  if(buf[2] == 31){
    ee = 2;
    }
  if(buf[2] == 32){
    ee = 3;
    }
  if(buf[2] == 33){
    ee = 4;
    }
 if(buf[2] == 34){
    ee = 5;
    }
  if(buf[2] == 35){
    ee = 6;
    }
 if(buf[2] == 36){
    ee = 7;
    }
  if(buf[2] == 37){
    ee = 8;
    }
  if(buf[2] == 38){
    ee = 9;
    }
  if(buf[2] == 39){
    ee = 0;
    }
  if(buf[2] == 40){
    }
  }


if(mark == 5){
  if(buf[2] == 30){
    ff = 1;
    }
  if(buf[2] == 31){
    ff = 2;
    }
  if(buf[2] == 32){
    ff = 3;
    }
  if(buf[2] == 33){
    ff = 4;
    }
 if(buf[2] == 34){
    ff = 5;
    }
  if(buf[2] == 35){
    ff = 6;
    }
 if(buf[2] == 36){
    ff = 7;
    }
  if(buf[2] == 37){
    ff = 8;
    }
  if(buf[2] == 38){
    ff = 9;
    }
  if(buf[2] == 39){
    ff = 0;
    }
  if(buf[2] == 40){
    }
  }

if(mark == 6){
  if(buf[2] == 30){
    gg = 1;
    }
  if(buf[2] == 31){
    gg = 2;
    }
  if(buf[2] == 32){
    gg = 3;
    }
  if(buf[2] == 33){
    gg = 4;
    }
 if(buf[2] == 34){
    gg = 5;
    }
  if(buf[2] == 35){
    gg = 6;
    }
 if(buf[2] == 36){
    gg = 7;
    }
  if(buf[2] == 37){
    gg = 8;
    }
  if(buf[2] == 38){
    gg = 9;
    }
  if(buf[2] == 39){
    gg = 0;
    }
  if(buf[2] == 40){
    }
  }
 
if(mark == 7){
  if(buf[2] == 30){
    hh = 1;
    }
  if(buf[2] == 31){
    hh = 2;
    }
  if(buf[2] == 32){
    hh = 3;
    }
  if(buf[2] == 33){
    hh = 4;
    }
 if(buf[2] == 34){
    hh = 5;
    }
  if(buf[2] == 35){
    hh = 6;
    }
 if(buf[2] == 36){
    hh = 7;
    }
  if(buf[2] == 37){
    hh = 8;
    }
  if(buf[2] == 38){
    hh = 9;
    }
  if(buf[2] == 39){
    hh = 0;
    }
  if(buf[2] == 40){
    }
  }

if(mark == 8){
  if(buf[2] == 30){
    ii = 1;
    }
  if(buf[2] == 31){
    ii = 2;
    }
  if(buf[2] == 32){
    ii = 3;
    }
  if(buf[2] == 33){
    ii = 4;
    }
 if(buf[2] == 34){
    ii = 5;
    }
  if(buf[2] == 35){
    ii = 6;
    }
 if(buf[2] == 36){
    ii = 7;
    }
  if(buf[2] == 37){
    ii = 8;
    }
  if(buf[2] == 38){
    ii = 9;
    }
  if(buf[2] == 39){
    ii = 0;
    }
  if(buf[2] == 40){
    }
  }

if(mark == 9){
  if(buf[2] == 30){
    jj = 1;
    }
  if(buf[2] == 31){
    jj = 2;
    }
  if(buf[2] == 32){
    jj = 3;
    }
  if(buf[2] == 33){
    jj = 4;
    }
 if(buf[2] == 34){
    jj = 5;
    }
  if(buf[2] == 35){
    jj = 6;
    }
 if(buf[2] == 36){
    jj = 7;
    }
  if(buf[2] == 37){
    jj = 8;
    }
  if(buf[2] == 38){
    jj = 9;
    }
  if(buf[2] == 39){
    jj = 0;
    }
  if(buf[2] == 40){
    }
  }

if(mark == 10){
  if(buf[2] == 30){
    kk = 1;
    }
  if(buf[2] == 31){
    kk = 2;
    }
  if(buf[2] == 32){
    kk = 3;
    }
  if(buf[2] == 33){
    kk = 4;
    }
 if(buf[2] == 34){
    kk = 5;
    }
  if(buf[2] == 35){
    kk = 6;
    }
 if(buf[2] == 36){
    kk = 7;
    }
  if(buf[2] == 37){
    kk = 8;
    }
  if(buf[2] == 38){
    kk = 9;
    }
  if(buf[2] == 39){
    kk = 0;
    }
  if(buf[2] == 40){
    }
  }

if(mark == 11){
  if(buf[2] == 30){
    ll = 1;
    }
  if(buf[2] == 31){
    ll = 2;
    }
  if(buf[2] == 32){
    ll = 3;
    }
  if(buf[2] == 33){
    ll = 4;
    }
 if(buf[2] == 34){
    ll = 5;
    }
  if(buf[2] == 35){
    ll = 6;
    }
 if(buf[2] == 36){
    ll = 7;
    }
  if(buf[2] == 37){
    ll = 8;
    }
  if(buf[2] == 38){
    ll = 9;
    }
  if(buf[2] == 39){
    ll = 0;
    }
  if(buf[2] == 40){
    }
  }


if(mark == 12){
  if(buf[2] == 30){
    mm = 1;
    }
  if(buf[2] == 31){
    mm = 2;
    }
  if(buf[2] == 32){
    mm = 3;
    }
  if(buf[2] == 33){
    mm = 4;
    }
 if(buf[2] == 34){
    mm = 5;
    }
  if(buf[2] == 35){
    mm = 6;
    }
 if(buf[2] == 36){
    mm = 7;
    }
  if(buf[2] == 37){
    mm = 8;
    }
  if(buf[2] == 38){
    mm = 9;
    }
  if(buf[2] == 39){
    mm = 0;
    }
  if(buf[2] == 40){
    }
  }

mark++;        

if(mark > 13){

Serial.print(aa);
Serial.print(bb);
Serial.print(cc);
Serial.print(dd);
Serial.print(ee);
Serial.print(ff);
Serial.print(gg);
Serial.print(hh);
Serial.print(ii);
Serial.print(jj);
Serial.print(kk);
Serial.print(ll);
Serial.println(mm);

mark = 0;
delay(5);
}}}
