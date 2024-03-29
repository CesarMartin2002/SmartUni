#include "pitches.h"
#include <Keypad.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <TimeLib.h>
#include <DHT.h>
#define BUZZZER_PIN  33 // PIN 32 CONECTADO AL BUZZER
#define DHTPIN 13 //Define the digital pin where the sensor is connected
#define DHTTYPE DHT11
//////////////////////////
//******DHT config******//
//////////////////////////
DHT dht(DHTPIN, DHTTYPE); //Initialize the DHT11 sensor
float t;
int temperatura;
int ran;
int randr;
bool actuando=false;
//////////////////////////
//*****WiFi config******//
//////////////////////////
#define WIFI_SSID "POCO F3"
#define WIFI_PASSWORD "12345678"
//////////////////////////
//*********Time*********//
//////////////////////////
#define TIME_HEADER  "T"   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 
/////////////////////////
//connection components//
/////////////////////////
String idTaquilla="2";
// String host="http://192.168.1.151:8000"; //LOMBA
//String host="http://192.168.116.148:8000"; //CESAR
String host="https://bottle-editing-licensed-kathy.trycloudflare.com"; //LUCÍA
String endpointLock=host+"/taquillas/"+idTaquilla;
String endpointHistorico=host+"/aulas/1/historico";
String endpointClimatizar=host+"/aulas/1/climatizar";
String endpointTemp=host+"/aulas/1";

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
int contador=0;
bool anterior=false;



void setup() {
  Serial.begin(1200);
  setup_wifi();
  pinMode(ledpin, OUTPUT);
  servo1.attach(12);
  dht.begin(); //Start the DHT sensor

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

    if(minute()%2==0 && second()==0 && actuando==false) {
      //cada 2 minutos entra en el codigo
      Serial.println("hago llamada de temp");
      if(llamadaClima()){
        actuando=true;
        ran=random(10, 20);
        randr = ran+minute();
      }
      //conexion con sistema aqui para luz y temp//
      delay(1000);
    }

    actualizaTemp();
    updateClima();
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
contador=0;
int distancia=readUltrasonicDistance(pinTrigger,pinEco);
servo1.write(0);
Serial.println("abro");
delay(2000);
while(contador<5){
    distancia=readUltrasonicDistance(pinTrigger,pinEco);
    Serial.println(distancia);
    if(distancia<=35){
      contador++;
      tone(BUZZZER_PIN, NOTE_C4, 100);
    }
    else{
      contador=0;
    }
    delay(1000);
  }
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
  return 0.1723*pulseIn(echoPin,HIGH);
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
  String msgLock = "{\"password\": \""+contra.substring(0,4)+"\"}";
  Serial.println(msgLock);
  HTTPClient http;
  http.begin(endpointLock);        //Indicamos el destino
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

void actualizaTemp(){
  HTTPClient http;
  if(minute()%2==0 && second()==10) {
    //cada 5 minutos entra en el codigo
    Serial.println("actualizo la temperatura");
    t = dht.readTemperature();
    temperatura = int(t);
    //llamada
    String dataTemp = "{\"temperatura\": \""+String(temperatura)+"\"}";
    http.begin(endpointTemp);        //Indicamos el destino
    http.addHeader("Content-Type", "application/json"); //Preparamos el header text/plain si solo vamos a enviar texto plano sin un paradigma llave:valor.
    //Enviamos el post pasándole, los datos que queremos enviar. (esta función nos devuelve un código que guardamos en un int)
    int codigo_respuesta = http.PUT(dataTemp);
    if(codigo_respuesta>0){
      Serial.println("Código HTTP ► " + String(codigo_respuesta));   //Print return code
      if(codigo_respuesta == 200){
        String cuerpo_respuesta = http.getString();
        Serial.println("El servidor respondió ▼ ");
        Serial.println(cuerpo_respuesta);
      }
    }else{
     Serial.print("Error enviando PUT endpointTemp, código: ");
     Serial.println(codigo_respuesta);
    }
    http.end();  //libero recursos
    delay(1000);
  }
}

void updateClima(){
  HTTPClient http;
  if(minute()==randr && second()==0 && actuando) {
    //cada 5 minutos entra en el codigo
    t = dht.readTemperature(); //Read temperatura in Celsius degrees
    temperatura = int(t);
    Serial.println("hago update en historico");
    //lamada post
    String dataClimatizar = "{\"id_aula_aula\":1,\"temperatura_previa\":"+String(temperatura)+",\"tiempo_calentar\":"+String(ran)+"}";
    http.begin(endpointHistorico);        //Indicamos el destino
    http.addHeader("Content-Type", "application/json"); //Preparamos el header text/plain si solo vamos a enviar texto plano sin un paradigma llave:valor.
    //Enviamos el post pasándole, los datos que queremos enviar. (esta función nos devuelve un código que guardamos en un int)
    int codigo_respuesta = http.POST(dataClimatizar);
    if(codigo_respuesta>0){
      Serial.println("Código HTTP ► " + String(codigo_respuesta));   //Print return code
      if(codigo_respuesta == 200){
        String cuerpo_respuesta = http.getString();
        Serial.println("El servidor respondió ▼ ");
        Serial.println(cuerpo_respuesta);
      }
    }else{
     Serial.print("Error enviando POST endpointHistorico, código: ");
     Serial.println(codigo_respuesta);
    }
    http.end();  //libero recursos
    delay(1000);
    actuando=false;
  }
}

bool llamadaClima(){
  HTTPClient http;
  http.begin(endpointClimatizar);        //Indicamos el destino
  http.addHeader("Content-Type", "application/json"); //Preparamos el header text/plain si solo vamos a enviar texto plano sin un paradigma llave:valor.
  //Enviamos el post pasándole, los datos que queremos enviar. (esta función nos devuelve un código que guardamos en un int)
  int codigo_respuesta = http.GET();
  if(codigo_respuesta>0){
      Serial.println("Código HTTP ► " + String(codigo_respuesta));   //Print return code
      if(codigo_respuesta == 200){
        String cuerpo_respuesta = http.getString();
        Serial.println("El servidor respondió ▼ ");
        Serial.println(cuerpo_respuesta);
      }
    }else{
     Serial.print("Error enviando GET endpointClimatizar, código: ");
     Serial.println(codigo_respuesta);
    }
  http.end();  //libero recursos
  return codigo_respuesta==200;
}
