#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;
Servo camera;

int vspeed = 20;
int vbase = 10;
int vshoulder = 90;
int velbow = 90;
int vwrist_rot = 90;
int vwrist_ver = 90;
int vgripper = 73;
int camera_position = 0;

int Hor = 0;
int Ver = 0;

void setup() {
  Serial.begin(9600);
  camera.attach(10);
  Braccio.begin();
  Braccio.ServoMovement(10, 10, 90, 90, 90, 90,  vgripper);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if(data == "Send position") {
      Serial.println(data + " wurde erkannt.");
      Serial.println(vbase);
      delay(50);
      Serial.println(vshoulder);
      delay(50);
      Serial.println(velbow);
      delay(50);
      Serial.println(vwrist_rot);
      delay(50);
      Serial.println(vwrist_ver);
      delay(50);
    } 
    else if(data == "Drive to") {
      Serial.println(data + " wurde erkannt. Es wird die Position angefahren.");
      data = Serial.readStringUntil('\n');
      vbase = data.toInt();
      delay(50);
      Serial.println(vbase);
      data = Serial.readStringUntil('\n');
      vshoulder = data.toInt();
      delay(50);
      Serial.println(vshoulder);
      data = Serial.readStringUntil('\n');
      velbow = data.toInt();
      delay(50);
      Serial.println(velbow);
      data = Serial.readStringUntil('\n');
      vwrist_rot = data.toInt();
      delay(50);
      Serial.println(vwrist_rot);
      data = Serial.readStringUntil('\n');
      vwrist_ver = data.toInt();
      delay(50);
      Serial.println(vwrist_ver);
      Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
    }
    else if(data == "Base 0") {
      //Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Base0();
    }
    else if(data == "Wachposition") {
      //Serial.println(data + " wurde erkannt. Roboter bewegt sich in die Wachposition");
      Wachposition();
    } 
    else if(data == "Greifen") {
      //Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      // delay(500);
      Position1();
      delay(500);
      Greiferauf();
      Position2();
      delay(800);
      Greiferzu();
      Position3();
      delay(500);
      Position3();
      delay(500);
      Position4();
      delay(500);
      Position5();
      delay(500);
      /* Position6();
      delay(500); */
      //Greiferauf();
      Serial.println("Roboter ist fertig");
    }
    else if(data == "Greifer zu") {
      //Serial.println(data + " wurde erkannt. Greifer wird geschlossen");
      Greiferzu();
    }
    else if(data == "Greifer auf") {
      //Serial.println(data + " wurde erkannt. Greifer wird geöffnet");
      Greiferauf();
    } 
    else if(data == "StarkLinks") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      StarkLinks();
    } 
    else if(data == "Links") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      Links();
    } 
    else if(data == "LeichtLinks") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      StarkLinks();
    } 
    else if(data == "StarkRechts") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      LeichtRechts();
    } 
    else if(data == "Rechts") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      Rechts();
    } 
    else if(data == "LeichtRechts") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      StarkRechts();
    } 
    else if(data == "StopHor") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gestoppt");
    } 
    else if(data == "Hoch") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      Hoch();
    } 
    else if(data == "Runter") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gedreht");
      Runter();
    } 
    else if(data == "StopVer") {
      Serial.println(data + " wurde erkannt. Der Roboter wird gestoppt");
    } 
    else if(data == "Teebeutel weg") {
      Abwurfposition();
      Greiferauf();
      Wachposition();
    } 
    else{
      Serial.println("You sent me the unknown command: " + data);
    } 
  }
}

void Greiferauf() {
    vgripper = 10;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Greiferzu() {
    vgripper = 73;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void StarkLinks() {
    vbase -= 5;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Links() {
    vbase -= 2;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void LeichtLinks() {
    vbase -= 1;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void StarkRechts() {
    vbase += 5;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Rechts() {
    vbase += 2;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void LeichtRechts() {
    vbase += 1;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Hoch() {
    //vbase -= 5;
    //Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Runter() {
    //vbase -= 5;
    //Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Base0() {
    vbase = 0;
    vshoulder = 90;
    velbow = 90;
    vwrist_rot = 90;
    vwrist_ver = 90;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position0() {
    vshoulder = 90;
    velbow = 90;
    vwrist_rot = 90;
    vwrist_ver = 90;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position1() {
    vbase = 180;
    vshoulder = 90;
    velbow = 105;
    vwrist_rot = 150;
    vwrist_ver = 90;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position2() {
    vbase = 180;
    vshoulder = 90;
    velbow = 111;
    vwrist_rot = 170;
    vwrist_ver = 80;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position3() {
    velbow -= 3;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position4() {
    vbase -= 15;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position5() {
    vshoulder -= 3;
    velbow -= 5;
    vwrist_rot -= 20;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position6() {
    vbase -= 10;
    velbow -= 10;
    vwrist_rot -= 10;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Wachposition() {
    vbase = 30;
    vshoulder = 90;
    velbow = 90;
    vwrist_rot = 110;
    vwrist_ver = 80;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Abwurfposition() {
    vbase = 150;
    vshoulder = 90;
    velbow = 111;
    vwrist_rot = 170;
    vwrist_ver = 80;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}