# 1 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
# 1 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
// < includes >------------------------------------------------------------------------------------

# 4 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2
# 5 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

# 7 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2
# 8 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

# 10 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

// < defines >-------------------------------------------------------------------------------------




// < global data >---------------------------------------------------------------------------------


// create an instance of the object
Adafruit_BMP280 g_bmp280;

// pressão base (QNH) (this should be adjusted to your local forcase)
float g_QNH = 1015;



// create an instance of the object
MPL3115A2 g_mpl3115;


// ------------------------------------------------------------------------------------------------
void setup()
{
    // join i2c bus
    Wire.begin();

    // start serial for output
    Serial.begin(9600);


    // BMP 280 init ok ?
    if (!g_bmp280.begin())
    {
        Serial.println((reinterpret_cast<const __FlashStringHelper *>((__extension__({static const char __c[] __attribute__((__progmem__)) = ("Could not find a valid BMP280 sensor, check wiring!"); &__c[0];})))));
        while (1);

    } // end if



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


} // setup

// ------------------------------------------------------------------------------------------------
void loop()
{
    // tempo inicial
    unsigned long lul_ini;

    // get initial time (ms)
    lul_ini = millis();

    // send altitude
    Serial.print("!@ALT#");

    Serial.print(g_bmp280.readAltitude(g_QNH));
    Serial.print("#");


    Serial.print(g_mpl3115.readAltitude());
    Serial.print("#");

    Serial.print(millis() / 1000.);
    Serial.println();

    // send pressure
    Serial.print("!@PRS#");

    Serial.print(g_bmp280.readPressure());
    Serial.print("#");


    Serial.print(g_mpl3115.readPressure());
    Serial.print("#");

    Serial.print(millis() / 1000.);
    Serial.println();

    // send temperature
    Serial.print("!@TMP#");

    Serial.print(g_bmp280.readTemperature());
    Serial.print("#");


    Serial.print(g_mpl3115.readTemp());
    Serial.print("#");

    Serial.print(millis() / 1000.);
    Serial.println();

    // 1Hz
    delay(1000 - (millis() - lul_ini));

} // loop

// < the end >-------------------------------------------------------------------------------------
