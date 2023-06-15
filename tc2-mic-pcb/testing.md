
## Audio
### Microphone
- https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-test
- `sudo apt install python3-pip`
- `sudo pip3 install --upgrade adafruit-python-shell`
- `wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py`
- `sudo python3 i2smic.py` Auto load at boot? Y, Reboot now? Y
- Drive GPI17 HIGH to stop LORA module from interfering with the microphone as some of the pins are used for moth modules.
- `python`


Might have to change pins.
```
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)
```