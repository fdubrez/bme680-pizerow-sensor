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

You must set a `.env` file with the right configuration to setup influxdb connectivity (dee `.env.template` file).

Simply run `python script.py`
