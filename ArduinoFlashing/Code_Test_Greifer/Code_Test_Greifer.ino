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
int vshoulder, velbow, vwrist_rot, vwrist_ver = 90;
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
    
    if(data == "Greifer zu") {
      Serial.println(data + " wurde erkannt. Greifer wird geschlossen");
      Greiferzu();
    }
    else if(data == "Greifer auf") {
      Serial.println(data + " wurde erkannt. Greifer wird geöffnet");
      Greiferauf();
    }
    /* else if(data == "Kamera 1") {
      Serial.println(data + " wurde erkannt. Kamera wird gedreht");
      while (camera_position <= 180) {
        camera.write(camera_position);
        delay(30);
        camera_position++;
      }
    }
    else if(data == "Kamera 2") {
      Serial.println(data + " wurde erkannt. Kamera wird gedreht");
      while (camera_position <= 0) {
        camera.write(camera_position);
        delay(30);
        camera_position--;
      }
    } */
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
    else if(data == "Base 0") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Base0();
    }
    else if(data == "Base 180") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Base180();
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
    else if(data == "Position 21") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position21();
    }
    else if(data == "Position 22") {
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
      Position22();
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
      Serial.println(data + " wurde erkannt. Roboter wird bewegt");
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
    }
    else{
      Serial.print("You sent me the unknown command: ");
      Serial.println(data);
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
void Base180() {
    vbase = 180;
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
void Position21() {
    vwrist_ver -= 10;
    Braccio.ServoMovement(vspeed, vbase, vshoulder, velbow, vwrist_rot, vwrist_ver,  vgripper);
}
void Position22() {
    vwrist_ver += 10;
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