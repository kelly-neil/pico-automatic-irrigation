## Raspberry Pi Pico Automatic Irrigation System

This project uses a Raspberry Pi Pico to monitor temperature, humidity, and soil moisture to sprinkle water at the appropriate time for optimal growth.

# Libraries:

Libraries used in the front-end:
- [ChartJS](https://www.chartjs.org/): will possibly be stripped down if ever it takes much space
- [PetiteVue](https://github.com/vuejs/petite-vue): light-weight framework for reusable components and data bindings

Libraries used in the back-end:
- [phew!](https://github.com/pimoroni/phew): light-weight web server for the Raspberry Pi Pico that includes preprocessing and routing

# Data recording:

Monitored data will be stored in their respective .csv files.
Variables are recorded every 1 minute.
Due to the limited storage capacity of the Pico, only data from the last 7 days will be kept.
Users will be able to export the data to a different device so to be able to keep the data.

# 
