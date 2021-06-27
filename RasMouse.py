import time
import numpy as np
import wiringpi as pi

SPI_CH = 0
READ_CH = 0
pi.wiringPiSPISetup(SPI_CH, 1000000 )

motor11_pin = 23
motor12_pin = 24
motor21_pin = 22
motor22_pin = 27
pi.wiringPiSetupGpio()
pi.pinMode( motor11_pin, 1 )
pi.pinMode( motor12_pin, 1 )
pi.pinMode( motor21_pin, 1 )
pi.pinMode( motor22_pin, 1 )
pi.softPwmCreate( motor11_pin, 0, 100)
pi.softPwmCreate( motor12_pin, 0, 100)
pi.softPwmCreate( motor21_pin, 0, 100)
pi.softPwmCreate( motor22_pin, 0, 100)
pi.softPwmWrite( motor11_pin, 0 )
pi.softPwmWrite( motor12_pin, 0 )
pi.softPwmWrite( motor21_pin, 0 )
pi.softPwmWrite( motor22_pin, 0 )

while True:
    try:
        pi.softPwmWrite( motor11_pin, 0 )
        pi.softPwmWrite( motor12_pin, 60 )
        pi.softPwmWrite( motor21_pin, 0 )
        pi.softPwmWrite( motor22_pin, 60 )
        
        buffer = 0x6800 |  (0x1800 * READ_CH ) 
        buffer = buffer.to_bytes( 2, byteorder='big' )
        
        pi.wiringPiSPIDataRW( SPI_CH, buffer )
        value = ( buffer[0] * 256 + buffer[1] ) & 0x3ff
        print ("value :" , value)
        if value > 1000:
            pi.softPwmWrite( motor11_pin, 0 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1)
            pi.softPwmWrite( motor11_pin, 60 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 60 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(0.8)
            pi.softPwmWrite( motor11_pin, 30 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, 30 )
            time.sleep(0.8)
            pi.softPwmWrite( motor11_pin, 0 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1)

    except KeyboardInterrupt:
        break

pi.softPwmWrite( motor11_pin, 0 )
pi.softPwmWrite( motor12_pin, 0 )
pi.softPwmWrite( motor21_pin, 0 )
pi.softPwmWrite( motor22_pin, 0 )

print('Stop Streaming')
