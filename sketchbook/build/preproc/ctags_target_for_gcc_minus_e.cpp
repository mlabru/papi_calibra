# 1 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
# 1 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
// < includes >------------------------------------------------------------------------------------

# 4 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2
# 5 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

# 7 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

# 9 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2
# 10 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

# 12 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

# 14 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino" 2

// < defines >-------------------------------------------------------------------------------------




// #define D_DEBUG

// wait time (1000/D_TIM_WAIT) = Hz


// < global data >---------------------------------------------------------------------------------


// create an instance of the object
Adafruit_BMP280 g_bmp280;

// pressão nível do mar (QNH) (this should be adjusted to your local forcase)
float g_QNH = 1015;



// create an instance of the object
MPL3115A2 g_mpl3115;



// create an instance of the object
TinyGPS g_gps;

SoftwareSerial g_ss(2, 3);


// ------------------------------------------------------------------------------------------------
void setup()
{
    // join i2c bus
    Wire.begin();

    // start serial for output
    Serial.begin(115200);


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
    // g_mpl3115.setModeAltimeter();

    // measure pressure in Pascals from 20 to 110 kPa
    g_mpl3115.setModeBarometer();

    // set oversample to the recommended 128
    g_mpl3115.setOversampleRate(7);


    // enable all three pressure and temp event flags
    g_mpl3115.enableEventFlags();



    // init GPS connection
    g_ss.begin(4800);


} // setup

// ------------------------------------------------------------------------------------------------
void loop()
{

    // altitude calc
    float lf_Px;
    float lf_off_h;

    // GPS new data
    bool lv_new_data = false;

    // GPS data
    float lf_lat;
    float lf_lon;

    unsigned long lul_age;

    // tempo inicial
    unsigned long lul_ini;
    // elapsed time
    unsigned long lul_elp;

    // get initial time (ms)
    lul_ini = millis();

    // send altitude
    Serial.print("!@ALT#");

    Serial.print(g_bmp280.readAltitude(g_QNH));
    Serial.print("#");


    // measure altitude above sea level in meters
    lf_Px = 1. - pow(g_mpl3115.readPressure() / 101325, 0.1902632);
    lf_off_h = 60.;

    Serial.print((44330.77 * lf_Px) + lf_off_h);
    Serial.print("#");

    Serial.print(millis() / 1000.);
    Serial.println();

    // send pressure
    Serial.print("!@BAR#");

    // send millibar pressure 
    Serial.print(g_bmp280.readPressure() / 100.);
    Serial.print("#");


    // send millibar pressure
    Serial.print(g_mpl3115.readPressure() / 100.);
    Serial.print("#");

    Serial.print(millis() / 1000.);
    Serial.println();

    // send temperature
    Serial.print("!@THR#");

    Serial.print(g_bmp280.readTemperature());
    Serial.print("#");


    Serial.print(g_mpl3115.readTemp());
    Serial.print("#");

    Serial.print(millis() / 1000.);
    Serial.println();


    // while data avaiable on RX...
    while (g_ss.available())
    {
        // read RX (GPS data)
        char l_ch = g_ss.read();

        // uncomment to see the GPS data flowing
        // Serial.write(l_ch);

        // did a new valid sentence come in ?
        if (g_gps.encode(l_ch))
            // set flag
            lv_new_data = true;

    } // end while

    if (lv_new_data)
    {
        g_gps.f_get_position(&lf_lat, &lf_lon, &lul_age);

        Serial.print("!@GPS#");
        Serial.print(lf_lat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : lf_lat, 6);
        Serial.print("#");
        Serial.print(lf_lon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : lf_lon, 6);
        Serial.print("#");
        Serial.print(g_gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : g_gps.satellites());
        Serial.print("#");
        Serial.print(g_gps.hdop() == TinyGPS::GPS_INVALID_HDOP ? 0 : g_gps.hdop());
        Serial.print("#");
        Serial.print(millis() / 1000.);
        Serial.println();

    } // end if
# 205 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
    // D_TIM_WAIT - elapsed time
    lul_elp = 500 /* 2 Hz*/ - (millis() - lul_ini);

    // adiantado ?
    if (lul_elp >= 0)
        // aguarda completar o tempo
        delay(lul_elp);

} // loop

// < the end >-------------------------------------------------------------------------------------
