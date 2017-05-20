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



// #define D_GPS
// #define D_DEBUG

// wait time (1000/D_TIM_WAIT) = Hz


// < global data >---------------------------------------------------------------------------------


// create an instance of the object
Adafruit_BMP280 g_bmp280;

// pressão nível do mar (QNH) (this should be adjusted to your local forcase)
float g_QNH = 1015;

// bias de altitude
float gf_alt_bmp = 0;



// create an instance of the object
MPL3115A2 g_mpl3115;

// bias de altitude
float gf_alt_mpl = 0;
# 53 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
// ------------------------------------------------------------------------------------------------
void setup()
{
    // join i2c bus
    Wire.begin();

    // start serial for output
    Serial.begin(57600);


    // BMP 280 init ok ?
    if (!g_bmp280.begin())
    {
        Serial.println((reinterpret_cast<const __FlashStringHelper *>((__extension__({static const char __c[] __attribute__((__progmem__)) = ("Could not find a valid BMP280 sensor, check wiring!"); &__c[0];})))));
        while (1);

    } // end if



    // init MPL3115
    setup_MPL3115();







    // calibração
    // calibra();

} // setup

// ------------------------------------------------------------------------------------------------
void loop()
{

    // altitude calc
    float lf_Px;
    float lf_off_h;
# 107 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
    // tempo inicial
    unsigned long lul_ini;
    // elapsed time
    unsigned long lul_elp;

    // get initial time (ms)
    lul_ini = millis();

    // send altitude
    Serial.print("!@ALT#");

    Serial.print(g_bmp280.readAltitude(g_QNH) - gf_alt_bmp);
    Serial.print("#");



    // measure altitude above sea level in meters
    lf_Px = 1. - pow(g_mpl3115.readPressure() / 101325, 0.1902632);
    lf_off_h = 60.;

    Serial.print(((44330.77 * lf_Px) + lf_off_h) - gf_alt_mpl);
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
# 207 "/home/mlabru/Public/mkr/papi/srce/papi_calibra/sketchbook/papi_sensors/papi_sensors.ino"
    // D_TIM_WAIT - elapsed time
    lul_elp = 500 /* 2 Hz*/ - (millis() - lul_ini);

    // adiantado ?
    if (lul_elp > 0)
        // aguarda completar o tempo
        delay(lul_elp);

} // loop

// ------------------------------------------------------------------------------------------------
void setup_MPL3115()
{
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

} // setup_MPL3115

// ------------------------------------------------------------------------------------------------
void calibra()
{

    // altitude calc
    float lf_Px;
    float lf_off_h;


    // tempo inicial
    unsigned long lul_ini;
    // elapsed time
    unsigned long lul_elp;

    for (int li_i = 0; li_i < 120; li_i++)
    {
        // get initial time (ms)
        lul_ini = millis();


        // obtém a altitude 
        gf_alt_bmp += g_bmp280.readAltitude(g_QNH);



        // measure altitude above sea level in meters
        lf_Px = 1. - pow(g_mpl3115.readPressure() / 101325, 0.1902632);
        lf_off_h = 60.;

        gf_alt_mpl += ((44330.77 * lf_Px) + lf_off_h);





        // D_TIM_WAIT - elapsed time
        lul_elp = 500 /* 2 Hz*/ - (millis() - lul_ini);

        // adiantado ?
        if (lul_elp > 0)
            // aguarda completar o tempo
            delay(lul_elp);

    } // end for


    // calcula a média
    gf_alt_bmp /= 120.;



    // calcula a média
    gf_alt_mpl /= 120.;


} // calibra

// < the end >-------------------------------------------------------------------------------------
