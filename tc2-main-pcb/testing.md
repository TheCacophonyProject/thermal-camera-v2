# Testing PCB

This is out of date but some parte might still be useful.

Fresh install of Raspberry Pi 64 Bit

## I2C

- `sudo apt install i2c-tools`
- `sudo raspi-conf` enable I2C
- `i2c detect -y 1`
- Check that you can see the addressed of all the devices
- Done

### Temp and Humidity Sensor

- Can get code to test sensor from [tc2-hat-software](https://github.com/TheCacophonyProject/tc2-hat-software)

### RTC

Add to `/etc/boot.conf` on raspberry pi

``` conf
# Enable RTC
dtoverlay=i2c-rtc,pcf8563
```

### Speaker

- Drive GPIO4 HIGH to enable speaker
- `python`

``` python
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)
```

- Follow [Adafruit setup instructions](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage)

### TODO

- EEPROM

## ATtiny1616

### ATtiny1616 RPi Setup

- `sudo apt install python3-pip -y`
- `pip install pymcuprog`
- Free up UART to be used for UPDI connection. Add `dtoverlay=disable-bt` to the end of `/boot/config.txt`
- Disable UART outputting to console: Remove `console=serial0,115200` from `/boot/cmdline.txt` and reboot.
- [pymcprog](https://github.com/microchip-pic-avr-tools/pymcuprog)
- Ping `sudo pymcuprog -d attiny1616 -t uart -u /dev/serial0 ping`
- Erase `sudo pymcuprog -d attiny1616 -t uart -u /dev/serial0 erase`
- Program through UPDI `sudo pymcuprog -d attiny1616 -t uart -u /dev/serial0 write -f ./Blink-attiny1616.ino.t1616.20c0.mD0.v261.hex`
- Note that you should Erase before programming each time.

### ATtiny1616 Testing

- [x] LED
- [] I2C minion
- [] RTC INT
- [] Battery voltage

### ATtiny1616 TODO

- [] Change programming to UPDI instead of ISP
- [] Fix LED pinout for colors
- [] Smaller resistors for LED

## Modem

- [Blog with setup instructions](https://www.elementzonline.com/blog/using-gps-antenna-with-sim7600-4g-lte-modem-v2-0)
- Enable by driving pin `4G_POWER_ON` HIGH
- [Waveshare wiki](https://www.waveshare.com/wiki/SIM7600G-H-M.2)
  - `sudo apt-get install minicom`
  - `sudo minicom -D /dev/ttyUSB2`
  - `AT+CUSBPIDSWITCH=9011,1,1`
  - `sudo dhclient -v usb0`
    AT+CMEE=2

### Modem Testing

- [x] GPS
- [x] 4G
