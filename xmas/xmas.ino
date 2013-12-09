
const int RED_PIN = 9;
const int GREEN_PIN = 10;
const int BLUE_PIN = 11;

char incomingByte = ' ';
String input_str = "";

void setup()
{
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  Serial.begin(9600);

}

void loop()
{
  int red;
  int green;
  int blue;
  
  if (Serial.available() > 0) {  
    char incomingByte = Serial.read();
    if (incomingByte == 'X'){
      if (input_str[0] == 'G'){
        red = input_str.substring(1, 4).toInt();
        green = input_str.substring(5, 8).toInt();
        blue = input_str.substring(9).toInt();
        analogWrite(RED_PIN, red);
        analogWrite(BLUE_PIN, blue);
        analogWrite(GREEN_PIN, green);
        delay(2000);
        input_str = "";
        
      } else {
          //analogWrite(RED_PIN, 255);
          red = input_str.substring(0, 3).toInt();
          green = input_str.substring(4, 7).toInt();
          blue = input_str.substring(8).toInt();
          analogWrite(RED_PIN, red);
          analogWrite(BLUE_PIN, blue);
          analogWrite(GREEN_PIN, green);
          input_str = "";
      }
    } 
    else {   
      input_str.concat(String(incomingByte));
    }   
  }
}


