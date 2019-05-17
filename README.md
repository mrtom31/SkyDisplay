# SkyDisplay

## Requirements:
- And OLED SSD1306 on i2c
- you need latest [luma.oled](https://luma-oled.readthedocs.io/en/latest/install.html)
- check if your device is available [here](https://github.com/rm-hull/luma.oled/wiki/Usage-&-Benchmarking)

## Installation & usage
### Install
```
cd ~
git clone https://github.com/mrtom31/SkyDisplay.git
cd SkyDisplay
```
### Usage
Check if it works first:
```
python OLEDSkycoinDisplay.py
```
Then use `crontab -e` to setup a schedule and add those lines:
```
* 8 * * * /home/pi/SkyDisplay/OLEDSkycoinDisplay.py
* 19 * * * kill $(cat /home/pi/SkyDisplay/pid.txt)
```
Replace `/home/pi` with the location where you cloned the repository.

Next profit!
