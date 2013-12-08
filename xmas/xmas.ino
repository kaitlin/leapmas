#include <SoftwareSerial.h>

SoftwareSerial mySerial(12, 13);

const int RED_PIN = 9;
const int GREEN_PIN = 10;
const int BLUE_PIN = 11;

int DISPLAY_TIME = 100;
int incomingByte = 0;
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
  if (Serial.available() > 0) {  
    char incomingByte = Serial.read();
    if (incomingByte == 'X'){
      if (input_str[0] == 'G'){
        int red = input_str.substring(1, 4).toInt();
        int green = input_str.substring(5, 8).toInt();
        int blue = input_str.substring(9, 12).toInt();
        analogWrite(RED_PIN, red);
        analogWrite(BLUE_PIN, blue);
        analogWrite(GREEN_PIN, green);
        delay(2000);
        input_str = "";
        
      } else {
        for (int x=0; x < input_str.length(); x++){
          
          if (input_str[x] == ';'){      
            char htemp[32];
            char stemp[32];   
            
            String hue = input_str.substring(0, x);
            hue.toCharArray(htemp, sizeof(htemp));
            float hue_fl = atof(htemp);
            
            String sat = input_str.substring(x+1, input_str.length()-1);
            sat.toCharArray(stemp, sizeof(stemp));
            float sat_fl = atof(stemp);
            long rgb = HSBtoRGB(hue_fl, sat_fl, 0.50);
            showRGB(rgb);
            input_str = "";  
            break;
          }
        }
      }
    } 
    else {   
      input_str.concat(String(incomingByte));
    }   
  }
}

void showRGB(int color)
{
  int redIntensity;
  int greenIntensity;
  int blueIntensity;

  // Here we'll use an "if / else" statement to determine which
  // of the three (R,G,B) zones x falls into. Each of these zones
  // spans 255 because analogWrite() wants a number from 0 to 255.

  // In each of these zones, we'll calculate the brightness
  // for each of the red, green, and blue LEDs within the RGB LED.

  if (color <= 255)          // zone 1
  {
    redIntensity = 255 - color;    // red goes from on to off
    greenIntensity = color;        // green goes from off to on
    blueIntensity = 0;             // blue is always off
  }
  else if (color <= 511)     // zone 2
  {
    redIntensity = 0;                     // red is always off
    greenIntensity = 255 - (color - 256); // green on to off
    blueIntensity = (color - 256);        // blue off to on
  }
  else // color >= 512       // zone 3
  {
    redIntensity = (color - 512);         // red off to on
    greenIntensity = 0;                   // green is always off
    blueIntensity = 255 - (color - 512);  // blue on to off
  }

  // Now that the brightness values have been set, command the LED
  // to those values

  analogWrite(RED_PIN, redIntensity);
  analogWrite(BLUE_PIN, blueIntensity);
  analogWrite(GREEN_PIN, greenIntensity);
}


long HSBtoRGB(float _hue, float _sat, float _brightness) {
    float red = 0.0;
    float green = 0.0;
    float blue = 0.0;
    
    if (_sat == 0.0) {
        red = _brightness;
        green = _brightness;
        blue = _brightness;
    } else {
        if (_hue == 360.0) {
            _hue = 0;
        }

        int slice = _hue / 60.0;
        float hue_frac = (_hue / 60.0) - slice;

        float aa = _brightness * (1.0 - _sat);
        float bb = _brightness * (1.0 - _sat * hue_frac);
        float cc = _brightness * (1.0 - _sat * (1.0 - hue_frac));
        
        switch(slice) {
            case 0:
                red = _brightness;
                green = cc;
                blue = aa;
                break;
            case 1:
                red = bb;
                green = _brightness;
                blue = aa;
                break;
            case 2:
                red = aa;
                green = _brightness;
                blue = cc;
                break;
            case 3:
                red = aa;
                green = bb;
                blue = _brightness;
                break;
            case 4:
                red = cc;
                green = aa;
                blue = _brightness;
                break;
            case 5:
                red = _brightness;
                green = aa;
                blue = bb;
                break;
            default:
                red = 0.0;
                green = 0.0;
                blue = 0.0;
                break;
        }
    }

    long ired = red * 255.0;
    long igreen = green * 255.0;
    long iblue = blue * 255.0;

  
    return long((ired << 16) | (igreen << 8) | (iblue));
}

