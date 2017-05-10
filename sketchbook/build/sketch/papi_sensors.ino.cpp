#include <Arduino.h>
#line 1 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
#line 1 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
// < includes >------------------------------------------------------------------------------------

#include <Wire.h>
#include <SPI.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#include "SparkFunMPL3115A2.h"

// < defines >-------------------------------------------------------------------------------------

#define D_BMP280   1
#define D_MPL3115  1

// < global data >---------------------------------------------------------------------------------

#ifdef D_BMP280
// create an instance of the object
Adafruit_BMP280 g_bmp280;

// pressão base (QNH) (this should be adjusted to your local forcase)
float g_QNH = 1015;
#endif

#ifdef D_MPL3115
// create an instance of the object
MPL3115A2 g_mpl3115;
#endif

// ------------------------------------------------------------------------------------------------
#line 32 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
void setup();
#line 72 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
void loop();
#line 32 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
void setup() 
{
    // join i2c bus
    Wire.begin();

    // start serial for output
    Serial.begin(9600);

#ifdef D_BMP280
    // BMP 280 init ok ?
    if (!g_bmp280.begin()) 
    {  
        Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
        while (1);

    } // end if
#endif // D_BMP280

#ifdef D_MPL3115
    // get sensor online
    g_mpl3115.begin();

    // configure the sensor

    // measure altitude above sea level in meters
    g_mpl3115.setModeAltimeter();

    // measure pressure in Pascals from 20 to 110 kPa
    // g_mpl3115.setModeBarometer();

    // set oversample to the recommended 128
    g_mpl3115.setOversampleRate(7);

    // enable all three pressure and temp event flags
    g_mpl3115.enableEventFlags();
#endif // D_MPL3115

} // setup

// ------------------------------------------------------------------------------------------------
void loop() 
{
#ifdef D_BMP280
    Serial.print("BMP280#");
    Serial.print(g_bmp280.readTemperature());
    Serial.print("#");
    Serial.print(g_bmp280.readPressure());
    Serial.print("#");
    Serial.print(g_bmp280.readAltitude(g_QNH));
    Serial.print("#");
    Serial.print(millis() / 1000.);
    Serial.println();
#endif // D_BMP280

#ifdef D_MPL3115
    Serial.print("MPL3115#");
    Serial.print(g_mpl3115.readTemp());
    Serial.print("#");
    Serial.print(g_mpl3115.readPressure());
    Serial.print("#");
    Serial.print(g_mpl3115.readAltitude());
    Serial.print("#");
    Serial.print(millis() / 1000.);
    Serial.println();
#endif // D_MPL3115

    // aguarda 1s
    delay(1000);

} // loop

// < the end >-------------------------------------------------------------------------------------
 
