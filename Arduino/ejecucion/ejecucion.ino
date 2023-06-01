#include "pitches.h"
#include <Keypad.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>
#include <WiFi.h>
#define BUZZZER_PIN  33 // PIN 32 CONECTADO AL BUZZER
//////////////////////////
//*****WiFi config******//
//////////////////////////
#define WIFI_SSID "POCO F3"
#define WIFI_PASSWORD "12345678"
/////////////////////////
//connection components//
/////////////////////////
String idTaquilla="2";
String host="http://192.168.1.151:8000";
String endpointLock="/taquillas/"+idTaquilla;
//////////////////////////
//***init components****//
//////////////////////////
const int ledpin=32;
Servo servo1;
int distancia=0;
int pinEco=26;
int pinTrigger=27;
//////////////////////////
//*****KEYPAD config****//
//////////////////////////
const byte ROWS = 4;
const byte COLS = 4;
char hexaKeys [ROWS][COLS]={
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
const int len_key = 4;
char attempt_key[len_key];
int z=0;//contador de teclas pulsadas
String contra;//attempt key convertida a int para eliminar letras
byte rowPins[ROWS] = {23,22,21,19};//row son los pines a negro
byte colPins[COLS] = {18,17,16,15};//col los pines a blanco
Keypad teclado =Keypad(makeKeymap(hexaKeys),rowPins,colPins,ROWS,COLS);
//////////////////////////
//*********misc*********//
//////////////////////////
/**
int horaNow=0;
int minNow=0;
**/

void setup() {
  Serial.begin(1200);
  setup_wifi();
  pinMode(ledpin, OUTPUT);
  servo1.attach(12);
  /**
  horaNow=hour();//obtenemos la hora actual
  minNow=minute();//obtenemos el minuto actual
**/
}

void loop() {

  if(WiFi.status()== WL_CONNECTED){   //comprobamos estado de la conexion WiFi 
    servo1.write(180);
    char key = teclado.getKey();
    if(key){
      digitalWrite(ledpin,HIGH);
      tone(BUZZZER_PIN, NOTE_D4, 100);
      delay(100);
      digitalWrite(ledpin,LOW);
      noTone(BUZZZER_PIN);
      attempt_key[z]=key;
      z++;
      if(z==4){
        contra=attempt_key;
        Serial.println(contra);
        if(llamadaLocker(contra)){
          Serial.println("abriendo caja");
          tonoAceptacion();
          abrirCaja();
          }
        else{
          Serial.println("la contrasena no coincide");
          tonoError();
        
        }
        z=0;
      }
    }
    /**
    //conditional para el sensor temp //
    //buscar como usar date en arduino //
    if((minNow<=minute()-5 && horaNow==hour()) || (horaNow<hour())){
      //si sigue siendo la misma hora y hace 5 minutos que no actualizamos los tiempos, o ha cambiado la hora consultamos
      horaNow=hour();//actualizamos la hora actual
      minNow=minute();//actualizamos el minuto actual

      //conexion con sistema aqui para luz y temp//

    }
    */
  }
  else{

     Serial.println("Error en la conexión WIFI");

  }


}

void tonoError(){
  for(int i=0;i<3;i++){   
    delay(100);       
    digitalWrite(ledpin,HIGH);
    tone(BUZZZER_PIN, NOTE_C4, 100);
    delay(100);
    digitalWrite(ledpin,LOW);
    noTone(BUZZZER_PIN);      
  }
}

void tonoAceptacion(){
  delay(150);
  tone(BUZZZER_PIN, NOTE_C4, 100);
  delay(150);
  noTone(BUZZZER_PIN);
  tone(BUZZZER_PIN, NOTE_D4, 200);
  noTone(BUZZZER_PIN);
}

void abrirCaja(){
  int distancia=readUltrasonicDistance(pinTrigger,pinEco);
  servo1.write(0);
  Serial.println("abro");
  delay(3000);
  Serial.println("cierro");
  servo1.write(180);
}

long readUltrasonicDistance(int triggerPin, int echoPin){
  //iniciamos el trigger en out
  pinMode(triggerPin,OUTPUT);
  //apagamos el emisor
  digitalWrite(triggerPin,LOW);
  delayMicroseconds(2);
  //emitimos
  digitalWrite(triggerPin,HIGH);
  delayMicroseconds(10);
  //apagamos
  digitalWrite(triggerPin,LOW);
  //escuchamos
  pinMode(echoPin,INPUT);
  return 0.01723*pulseIn(echoPin,HIGH);
}

//*****************************
//***    CONEXION WIFI      ***
//*****************************
void setup_wifi(){
	delay(10);
	// Nos conectamos a nuestra red Wifi
	Serial.println();
	Serial.print("Conectando a ssid: ");
	Serial.println(WIFI_SSID);

	WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
		Serial.print(".");
	}

	Serial.println("");
	Serial.println("Conectado a red WiFi!");
	Serial.println("Dirección IP: ");
	Serial.println(WiFi.localIP());
}

bool llamadaLocker(String contra){
  String msgLock = "{\"password\": \""+contra+"\"}";
  HTTPClient http;
  http.begin(host+endpointLock);        //Indicamos el destino
  http.addHeader("Content-Type", "application/json"); //Preparamos el header text/plain si solo vamos a enviar texto plano sin un paradigma llave:valor.
  //Enviamos el post pasándole, los datos que queremos enviar. (esta función nos devuelve un código que guardamos en un int)
  int codigo_respuesta = http.POST(msgLock);
  //conexion con el back para contraseña//
  if(codigo_respuesta>0){
    Serial.println("Código HTTP ► " + String(codigo_respuesta));   //Print return code
    if(codigo_respuesta==200){
      String cuerpo_respuesta = http.getString();
      Serial.println("El servidor respondió ▼ ");
      Serial.println(cuerpo_respuesta);
    }    
    http.end();  //libero recursos
    return codigo_respuesta==200;  
  }
}