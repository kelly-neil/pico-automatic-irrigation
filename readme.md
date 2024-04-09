## Raspberry Pi Pico Automatic Irrigation System

A capstone project which uses a Raspberry Pi Pico to monitor temperature, humidity, and soil moisture to sprinkle water at a specific soil moisture for optimal growth. It is written in MicroPython.

**This project is not designed for regular use.** Some issues are yet to be fixed, so it is not guaranteed that this project will **consistently** perform as intended.

# Libraries:

- [ChartJS](https://www.chartjs.org/) - displays graphs for monitoring data
- [PetiteVue](https://github.com/vuejs/petite-vue) - a lightweight JS library. It is tiny enough to fit in the Pico's limited flash memory that it can be used for the web app offline.
- Slight modified version of [phew!](https://github.com/pimoroni/phew): a web server designed for the Pico.

# Data recording:

Monitored data will be stored in their respective .csv files.
Variables are recorded every 1 minute.
Due to the limited storage capacity of the Pico, only data from the last 7 days will be kept.
Users will be able to export the data to a different device so to be able to keep the data.