#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int vspeed = 20;
int vbase = 10;
int vshoulder, velbow, vwrist_rot, vwrist_ver = 90;
int vgripper = 73;

void setup() {
  Serial.begin(9600);
  Braccio.begin();
  Braccio.ServoMovement(10, 10, 90, 90, 90, 90,  vgripper);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
    
    if(data == "Greifer zu") {
      Serial.println(data + " wurde erkannt. Greifer wird geschlossen");
      Greiferzu();
    }
    else if(data == "Greifer auf") {
      Serial.println(data + " wurde erkannt. Greifer wird geöffnet");
      Greiferauf();
    }
    else if(data == "Rechts 90") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      vbase += 90;
      Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
    }
    else if(data == "Links 90") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      vbase -= 90;
      Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
    }
    else if(data == "Position 0") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position0();
    }
    else if(data == "Position 1") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position1();
    }
    else if(data == "Position 2") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position2();
    }
    else if(data == "Position 3") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position3();
    }
    else if(data == "Position 4") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position4();
    }
    else if(data == "Position 5") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position5();
    }
    else if(data == "Greifen") {
      delay(3000);
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position1();
      delay(500);
      Greiferauf();
      Position2();
      delay(800);
      Greiferzu();
      Position3();
      delay(500);
      Position4();
      delay(500);
      Position5();
      delay(500);
      Position1();
      delay(500);
      Greiferauf();
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
void Position0() {
    vbase = 10;
    vshoulder = 90;
    velbow = 90;
    vwrist_rot = 90;
    vwrist_ver = 90;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position1() {
    vbase = 0;
    vshoulder = 90;
    velbow = 105;
    vwrist_rot = 150;
    vwrist_ver = 90;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position2() {
    vbase = 10;
    vshoulder = 93;
    velbow = 110;
    vwrist_rot = 175;
    vwrist_ver = 100;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position3() {
    vbase = 10;
    vshoulder = 93;
    velbow = 110;
    vwrist_rot = 170;
    vwrist_ver = 100;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position4() {
    vbase = 0;
    vshoulder = 93;
    velbow = 110;
    vwrist_rot = 170;
    vwrist_ver = 100;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position5() {
    vbase = 0;
    vbase = 0;
    vshoulder = 90;
    velbow = 105;
    vwrist_rot = 150;
    vwrist_ver = 90;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}




