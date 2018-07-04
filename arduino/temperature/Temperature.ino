void setup()
{
    Serial.begin(9600);
}

float tempC(int lmPin)
{
    float raw = analogRead(lmPin);
    float percent = raw / 1023.0;
    float volts = percent * 5.0;
    return 100.0 * volts;
}

void loop()
{
    float total = 0;
    int count = 10;
    for (int i=0; i<count; i++) {
        total += tempC(A0);
        delay(1000);
    }

    float temp = total / count;

    Serial.print("{\"A0\": ");
    Serial.print(temp);
    Serial.print(",\"temperature\": ");
    Serial.print(temp);
    Serial.println("}");

    delay(1000);
}
