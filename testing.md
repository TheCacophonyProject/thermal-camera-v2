# Testing PCB

## I2C
- `sudo apt install i2c-tools`
- `sudo raspi-conf` enable I2C
- `i2c detect -y 1`
- Check that you can see the addressed of all the devices
- Done
### Magnetic Sensor
- Can read data
- //TODO: Need to remove copper around sensor.

### Temp and Humidity Sensor
- Done

### RTC
```
# Enable RTC
dtoverlay=i2c-rtc,pcf8563
```
### TODO
- [] Smaller diodes


## Audio
### Microphone
- https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-test
- `sudo apt install python3-pip`
- `sudo pip3 install --upgrade adafruit-python-shell`
- `wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py`
- `sudo python3 i2smic.py` Auto load at boot? Y, Reboot now? Y
- Drive GPI17 HIGH to stop LORA module from interfering with the microphone as some of the pins are used for moth modules.
- `python`
```
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)
``` 

### Speaker
- Drive GPIO4 HIGH to enable speaker
- `python`
```
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)
```
### TODO 
- Nothing

## Lepton
- Need to enable pins for module to work
    - Enable lepton power
    - GPIO12 powerDownPin
    - GPIO13 resetPin
    - GPIO6 clkEnPin
### TODO
- Nothing

## Buzzer
- Driven by Pi and ATtiny
- Change to internal driven one.
### TODO
- [] Can be driven by Pi or ATtiny

## ATtiny1616
### Setup
- https://github.com/SpenceKonde/megaTinyCore/blob/master/Installation.md
- https://github.com/microchip-pic-avr-tools/pymcuprog
- Ping `~/.local/bin/pymcuprog -d attiny1616 -t uart -u /dev/serial0 ping`
- Program through UPDI `~/.local/bin/pymcuprog -d attiny1616 -t uart -u /dev/serial0 write -f ./Blink-attiny1616.ino.t1616.20c0.mD0.v261.hex`

### Testing
- [x] LED
- [] I2C minion
- [] RTC INT
- [] Battery voltage

### TODO
- [] Chage programming to UPDI instead of ISP
- [] Fix LED pinout for colors
- [] Smaller resistors for LED

## Modem
- https://www.elementzonline.com/blog/using-gps-antenna-with-sim7600-4g-lte-modem-v2-0
- Enable by driving pin `4G_POWER_ON` HIGH
- From https://www.waveshare.com/wiki/SIM7600G-H-M.2
    - `sudo apt-get install minicom`
    - `sudo minicom -D /dev/ttyUSB2`
    - `AT+CUSBPIDSWITCH=9011,1,1`
    - `sudo dhclient -v usb0`
### Testing
- [x] GPS
- [x] 4G
### TODO
- Nothing

## LORA
### Testing
- [] Antenna
- [] Connection
