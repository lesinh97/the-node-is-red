#include <Arduino.h>

// void setup() {  
//     Serial.begin(9600);  
//     uint32_t endTime = millis() + 10000;  
//     uint32_t count = 0;  
//     while (millis() < endTime)  
//         count++;  
//     Serial.print("Count: ");  
//     Serial.println(count);  
// }  

char ch = 'char'; // Variable stored char
String str = "str"; // Variable stored string
String conc; // String for concatenation

bool test = true; // Run test bit

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (test){ // Runs only once
   
////////////  COMPARISON OF PREMADE AND AUTO CONCATENATION //////////////////
    conc = String(ch+'_'+str+"_");
    Serial.print(conc); // BUG HERE
    Serial.print('\n');
    Serial.print(ch+'_'+str+"_"); // BUG HERE
    Serial.print('\n');
/////////// FIX BY STRING CONVERSION /////////////////////
    // Serial.print(String(ch)+'_'+str+"_");
    // Serial.print('\n');
    // Serial.print('\n');
/////////// TESTING SINGLE CHAR CONVERSION //////////////////////
    // Serial.print('char');
    // Serial.print('\n');
    // Serial.print(ch);
    // Serial.print('\n');
    // Serial.write('char');
    // Serial.print('\n');
    // Serial.write(ch);
    // Serial.print('\n');
    // Serial.print('\n');
/////////// TESTING WITHOUT CHAR VARIABLE /////////////////////
    Serial.print('char'+'_'+str+"_"); // BUG HERE
    Serial.print('\n');
    // Serial.print('\n');
/////////// TESTING WITHOUT VARIABLES ///////////////////
    Serial.print('char'+'_'+"str"+"_"); //SYNTAX ERROR
    //Serial.print('\n');
    //Serial.print('\n');
/////////// TESTING WITH ONLY STRING CONSTANTS //////////
    Serial.print("A"+"_"+"str"+"_"); //SYNTAX ERROR
    //Serial.print('\n');
    Serial.print('\n');
/////////// TESTING WITH ONLY CHAR CONSTANTS /////////////
    Serial.print('char'+'_'+'char'+'s'+'d'+'_'); // BUG HERE
    Serial.print('\n');
    // Serial.print('\n');
/////////// TESTING WITH NO ADJACENT CHARS /////////////
    Serial.print('char'+"str"+'B'+str); // BUG HERE
    Serial.print('\n');
    Serial.print('char'+"str"+str+'B'); // BUG HERE
    Serial.print('\n');
    // Serial.print('\n');
/////////// TESTING WITH STRING START /////////////
    // Serial.print(str+'char'+'_'+'char'+'s'+'d'+'_');
    // Serial.print('\n');
    Serial.print("str"+'char'+'_'+'char'+'s'+'d'+'_'); // BUG HERE
    Serial.print('\n');
    // Serial.print(str+'char');
    // Serial.print('\n');
    Serial.print("str"+'char'); // BUG HERE
    // Serial.print('\n');
    // Serial.print(str+ch);
    // Serial.print('\n');
    Serial.print("str"+ch); // BUG HERE
    // Serial.print('\n');
    Serial.print('\n');
////////// TESTING STRING CONST+VAR ///////////////
    Serial.print("str"+str);
    Serial.print('\n');
    Serial.print(str+"str");
    Serial.print('\n');
    Serial.print('\n');
    test = false;
  }
}
