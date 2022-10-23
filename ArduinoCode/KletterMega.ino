int stm[8];  //Array für die Datenspeicherung
void setup() {
  Serial.begin(9600);
  //Serial.println("Neue Messung");  //Markierung der neuen Messung
  pinMode(3, OUTPUT);              //Pin 2 initialisieren und auf High schalten, damit die Sensoren mit Strom versorgt werden
  digitalWrite(3, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  stm[0] = analogRead(A7);        //Array mit aktuellen Messwerten belegen
  stm[1] = analogRead(A6);
  stm[2] = analogRead(A5);
  stm[3] = analogRead(A4);
  stm[4] = analogRead(A3);
  stm[5] = analogRead(A2);
  stm[6] = analogRead(A1);
  stm[7] = analogRead(A0);

  for (int i = 0; i < 8; i++) {
    if (stm[i]<100) stm[i] = 0;
    Serial.print(stm[i]);       //aktuelle Daten in den seriellen Monitor schreiben
    Serial.print(",");
  }
  Serial.println("");
}
