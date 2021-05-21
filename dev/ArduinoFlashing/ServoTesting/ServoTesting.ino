#include <Servo.h>

Servo servo1;
int position1 = 0;
bool rotation_direction = false;

void setup()
{
  servo1.attach(10);
}
void loop(){
    /* if (position1 >= 180) {
        position1 = 0;
    } */
    if (rotation_direction == false)
    {
        while (position1 <= 180) {
            servo1.write(position1);
            delay(30);
            position1++;
        }
        rotation_direction = true;
    } 
    if (rotation_direction == true){
        while (position1 >= 0) {
            servo1.write(position1);
            delay(30);
            position1--;
        }
        rotation_direction = false;
    }
} 