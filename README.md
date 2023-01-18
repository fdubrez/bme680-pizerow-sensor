## Description

This project explain how to setup a [BME680](https://shop.pimoroni.com/products/bme680-breakout?variant=12491552129107) Temperature/Humidity/Pressure/Air quality sensor on a raspberry pi zero w and send it's data to a influxdb/grafana.

## Getting started

We assume you have `python3` installed on your system

```shell
# create Python virtual env
python -m venv venv
# use it
. venv/bin/activate
# install dependencies
python -m pip install -r requirements.txt
```

You must set a `.env` file with the right configuration to setup influxdb connectivity (see `.env.template` file).

Simply run `python script.py`

## Save outside temperature

Save outside temperature using openweather API.

Windows powershell:

```
PS C:\Users\fdubrez\git\github\bme680-pizerow-sensor> $env:OPENWEATHER_APPID='******'; $env:INFLUX_DB_BUCKET='<bucket>'; $env:INFLUX_DB_URL='http://<IP>:8086'; $env:INFLUX_DB_ORG='<org>'; $env:INFLUX_DB_MEASUREMENT_LOCATION='exterior'; $env:INFLUX_DB_TOKEN='<token>'; python .\weather.py -lat <lat> -long <long> --store
temperature is 3.08
```
