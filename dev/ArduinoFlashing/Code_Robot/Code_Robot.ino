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
      data = Serial.readStringUntil('\n');
      vbase = data.toInt();
      Serial.println(vbase);
      data = Serial.readStringUntil('\n');
      vshoulder = data.toInt();
      Serial.println(vshoulder);
      data = Serial.readStringUntil('\n');
      velbow = data.toInt();
      Serial.println(velbow);
      data = Serial.readStringUntil('\n');
      vwrist_rot = data.toInt();
      Serial.println(vwrist_rot);
      data = Serial.readStringUntil('\n');
      vwrist_ver = data.toInt();
      Serial.println(vwrist_ver);
      Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
    }
    else if(data == "Base 0") {
      //Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Base0();
    }
    else if(data == "Greifen") {
      //Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      delay(500);
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
      Position6();
      delay(500);
      Greiferauf();
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
    else if(data == "Links") {

    } 
    else if(data == "Rechts") {

    } 
    else if(data == "StopHor") {

    } 
    else if(data == "Hoch") {

    } 
    else if(data == "Runter") {

    } 
    else if(data == "StopVer") {

    } 
    else{
      //Serial.print("You sent me the unknown command: ");
      //Serial.println(data);
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
    vbase -= 10;
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