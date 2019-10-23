#include <AFMotor.h>
AF_DCMotor motor_l(3);
AF_DCMotor motor_r(4);
AF_DCMotor motor_pump(1);

void setup(){
  Serial.begin(9600);
  motor_l.setSpeed(200);
  motor_l.run(RELEASE);
  motor_r.setSpeed(200);
  motor_r.run(RELEASE);
  motor_pump.setSpeed(200);
 motor_pump.run(RELEASE);

}

void up()
{ 
  uint8_t i;
  Serial.println('up');

  // Turn on motor
  motor_l.run(FORWARD);
  motor_r.run(FORWARD);
  // Accelerate from zero to maximum speed
  for (i=0; i<255; i++) 
  {
    motor_l.setSpeed(i);
    motor_r.setSpeed(i);  
    delay(04);
  }
  
  // Decelerate from maximum speed to zero
  for (i=255; i!=0; i--) 
  {
    motor_l.setSpeed(i); 
    motor_r.setSpeed(i);  
    delay(04);
  }

  // Now change motor direction
 

  // Now turn off motor
  motor_l.run(RELEASE);
  motor_r.run(RELEASE);
  
}

/*left....*/

void left()
{
  
   motor_r.run(FORWARD);
    uint8_t i;
  for (i=0; i<255; i++) 
  {
    //motor_l.setSpeed(i);  
    motor_r.setSpeed(i); 
    delay(6);
  }
  
  // Decelerate from maximum speed to zero
  for (i=255; i!=0; i--) 
  {
    //motor_l.setSpeed(i);  
    motor_r.setSpeed(i); 
    delay(6);
  }
   motor_r.run(RELEASE);
   
}

/*right....*/


void right()
{
    motor_l.run(FORWARD);
    uint8_t i;
  for (i=0; i<255; i++) 
  {
    motor_l.setSpeed(i);  
    //motor_r.setSpeed(i); 
    delay(6);
  }
  
  // Decelerate from maximum speed to zero
  for (i=255; i!=0; i--) 
  {
    motor_l.setSpeed(i);  
    //motor_r.setSpeed(i); 
    delay(6);
  }
   motor_l.run(RELEASE);
} 


/*stp.....*/


void stp()
{
    uint8_t i;
    motor_l.setSpeed(0);
     motor_r.setSpeed(0);
  for (i=0; i<200; i++) 
  {
    
    delay(10);
  }
  
  // Decelerate from maximum speed to zero
  for (i=200; i!=0; i--) 
  {
   
    delay(10);
  }
}
void down() {

  uint8_t i;
 // Now change motor direction
  motor_l.run(BACKWARD);
   motor_r.run(BACKWARD);
  
  // Accelerate from zero to maximum speed
  for (i=0; i<255; i++) 
  {
    motor_l.setSpeed(i); 
     motor_r.setSpeed(i);  
    delay(4);
  }

  // Decelerate from maximum speed to zero
  for (i=255; i!=0; i--) 
  {
    motor_l.setSpeed(i);
     motor_r.setSpeed(i);  
    delay(4);
  }

  // Now turn off motor
  motor_l.run(RELEASE);
  motor_r.run(RELEASE);





}

/*pump off code......*/

void pump_on() {

  motor_pump.run(FORWARD);
  motor_pump.setSpeed(200);
  delay(50000);


}

void pump_off() {
   motor_pump.run(RELEASE);
   delay(100);


}


void loop(){
  if(Serial.available()){
    int message = Serial.read() - '0';
    // control the servo
    Serial.println(message);
    if(message==3) {
    
      up();
      delay(5);
    }
    if(message==4) {
      down();
      delay(5);
    }
    if(message == 5) {
      left();
      Serial.println(message);
      delay(5);
    }
    if(message==6) {
      right();
      Serial.println(message);
      delay(5);
    }
    if(message==7) {
      stp();
      delay(5);
    }
    if(message==8) {
      pump_on();
      delay(5);
      
    }
    if(message==9) {
      pump_off();
      delay(5);
    }
   
  }
}
