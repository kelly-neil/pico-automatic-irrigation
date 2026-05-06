## Raspberry Pi Pico Automatic Irrigation System

Code written for our Capstone project in Davao Chong Hua High School. This uses a Raspberry Pi Pico to monitor temperature, humidity, and soil moisture to sprinkle water at a specific soil moisture for optimal growth. It is written in MicroPython.

**This project is not designed for regular use.** Some issues are yet to be fixed, so it is not guaranteed that this project will **consistently** perform as intended.

# Libraries:

- [PetiteVue](https://github.com/vuejs/petite-vue) - a lightweight JS library. It is tiny enough to fit in the Pico's limited flash memory that it can be used for the web app offline.
- Slight modified version of [phew!](https://github.com/pimoroni/phew): a MicroPython web server designed for the Pico.

# Data recording:

Monitored data will be stored in their respective .csv files.
Variables are recorded every 10 seconds by default.
Users will be able to download the data from a web browser using a client device.