# Raspberry Pi Pico Automatic Irrigation System

*Please note that the code has several issues left unfixed as I no longer have the project with me.*

### About this project

This repository contains the code written for a watering system using the [Pico W](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico1) as the microcontroller board. Main features include:
- Switches water pump on when soil moisture reaches threshold
- Records temperature and humidity in intervals into an SD card
- Provides a web app via LAN that displays live and historical data

The project uses [phew!](https://github.com/pimoroni/phew) for the web server, and [petite-vue](https://github.com/vuejs/petite-vue) as the frontend library.

### Installation

Flash your Pico W with the [MicroPython firmware](https://micropython.org/download/RPI_PICO_W/), and simply upload the files to the filesystem.

The code assumes you've connected the pins as seen in this [circuit diagram](/circuit_diagram.jpg).