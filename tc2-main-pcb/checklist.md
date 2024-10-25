# KiCAD Checklist for tc2-main-pcb

## High Priority
- [ ] Add smaller SMD nut for the modem as it is on the underside and might fall off. Also make it so no copper is on the other side to conduct through the heat when going through the oven.
- [ ] Add battery JLC number
- [x] Add 12 pin power connector JLC number
- [x] Move mounting hole above Modem
- [x] Move LED and button down a mm

## Future Enhancements
- [ ] Bed of nails pads for testing
- [ ] Reduce power usage in sleep mode
- [ ] Disable UART multiplexer chip when Raspberry pi is powered off
- [ ] Make issue about single lable not causing errors when the single lable is attached to multiple pins
- [x] Improve crystal time
- [ ] Add Cacophony logo
- [ ] Add version variable on PCB when it can be set through kicad-cli

## Pre-release checklist
- [ ] Check pinout to power board matches
- [ ] Set TAG
- [ ] Check that components have LCSC part numbers

