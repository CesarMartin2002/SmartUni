#include "pitches.h"
#include <Keypad.h>
#include <ESP32Servo.h>
#include <PubSubClient.h>
#include <WiFi.h>
#define BUZZZER_PIN  33 // PIN 32 CONECTADO AL BUZZER
//////////////////////////
//*****WiFi config******//
//////////////////////////
#define WIFI_SSID "POCO F3"
#define WIFI_PASSWORD "12345678"
//////////////////////////
//*****mqtt config******//
//////////////////////////
/**
const char* mqtt_server="";//host al que conectar
const int mqtt_port=;//puerto al que conectar
const char* mqtt_user="";//user para conectarse
const char* mqtt_pass="";//pass del user
const char* root_topic_subscribe="";//topico para recibir mensajes
const char* root_topic_publish="";//topico para enviar mensajes
const byte ROWS = 4;
const byte COLS = 4;
**/
/////////////////////////
//connection components//
/////////////////////////
WiFiClient espClient;
PubSubClient client(espClient);
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
int master_key=1234;//esto se borrara cuando este listo el paso de mensajes
char attempt_key[len_key];
int z=0;//contador de teclas pulsadas
int contra;//attempt key convertida a int para eliminar letras
byte rowPins[ROWS] = {23,22,21,19};//row son los pines a negro
byte colPins[COLS] = {18,17,16,15};//col los pines a blanco
Keypad teclado =Keypad(makeKeymap(hexaKeys),rowPins,colPins,ROWS,COLS);
//////////////////////////
//*********misc*********//
//////////////////////////
int horaNow=0;
int minNow=0;

int id=1;   //id de la taquilla


void setup() {
  Serial.begin(1200);
  pinMode(ledpin, OUTPUT);
  servo1.attach(12);
  horaNow=hour();//obtenemos la hora actual
  minNow=minute();//obtenemos el minuto actual

}

void loop() {

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
      contra=String(attempt_key).toInt();
      Serial.println(contra);
      //conexion con el back para contraseña//
      if(contra==master_key){
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
  //conditional para el sensor temp //
  //buscar como usar date en arduino //
  if((minNow<=minute()-5 && horaNow==hour()) || (horaNow<hour())){
    //si sigue siendo la misma hora y hace 5 minutos que no actualizamos los tiempos, o ha cambiado la hora consultamos
    horaNow=hour();//actualizamos la hora actual
    minNow=minute();//actualizamos el minuto actual

    //conexion con sistema aqui para luz y temp//

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

void initWifi(){
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("Connected to the WiFi");
}