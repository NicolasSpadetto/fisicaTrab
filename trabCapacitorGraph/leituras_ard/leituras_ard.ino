

#define capRead A0
#define gndRef A1
#define Vcc 2        //pino digital que alimenta com 5v
#define Cap 0.0001F  //100uF, o F é para float
#define Resistor 4700
#define pwmPeriodo 6.0F
#define pwmDC 50.0F

unsigned long start;
bool reset = 1;
 
void pwmChager() 
{
  if (reset) 
  {
    start = millis();
    digitalWrite(Vcc, HIGH);
    reset = !(reset);
  } 
  else if (((millis() - start) / 1000.0) >= (pwmPeriodo * pwmDC / 100.0))
  {
    digitalWrite(Vcc, LOW);
    if (((millis() - start) / 1000.0) >= pwmPeriodo) reset = !(reset);
  }
}



void setup() 
{
  Serial.begin(9600);

  pinMode(Vcc, OUTPUT);
  digitalWrite(Vcc, LOW);
  pinMode(capRead, INPUT);
  pinMode(gndRef, INPUT);

  delay(5000);
}

float dif_pot;

void loop() 
{
  pwmChager();

  dif_pot = (analogRead(capRead) - analogRead(gndRef)) * (5.0 / 1023);
 
  
  Serial.print(dif_pot);
  Serial.print(" ");
  Serial.print(millis() - start);
  Serial.println();

  delay(Cap * Resistor * 100);  // pra ser humanamente possível de acompanhar
}