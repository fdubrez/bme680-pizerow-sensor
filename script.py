from datetime import datetime
import os
import argparse
import time

from dotenv import load_dotenv
import bme680
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


parser = argparse.ArgumentParser(description="Retrieve measurements from BME680 sensor and store them in an influxdb database")
parser.add_argument("--verbose", "-v", action="count", default=0)
args = parser.parse_args()

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

data = {
    "temperature": 21.0,
    "pressure": 21.0,
    "humidity": 21.0,
    "gas_resistance": 21.0
}

# we wait for data to be available
while sensor.get_sensor_data() is False or sensor.data.heat_stable is False:
    time.sleep(1)

data["temperature"] = float(format(sensor.data.temperature, "0.2f"))
data["pressure"] = float(format(sensor.data.pressure, "0.2f"))
data["humidity"] = float(format(sensor.data.humidity, "0.2f"))
data["gas_resistance"] = int(sensor.data.gas_resistance)
print(f"{data['temperature']} C, {data['pressure']} hPa, {data['humidity']} %RH, {data['gas_resistance']} Ohms")

load_dotenv()
INFLUX_DB_URL = os.getenv("INFLUX_DB_URL")
INFLUX_DB_TOKEN = os.getenv("INFLUX_DB_TOKEN")
INFLUX_DB_ORG = os.getenv("INFLUX_DB_ORG")
INFLUX_DB_BUCKET = os.getenv("INFLUX_DB_BUCKET")
INFLUX_DB_MEASUREMENT_LOCATION = os.getenv("INFLUX_DB_MEASUREMENT_LOCATION")

with InfluxDBClient(
    url=INFLUX_DB_URL,
    token=INFLUX_DB_TOKEN,
    org=INFLUX_DB_ORG,
    debug=True if args.verbose > 0 else False,
) as client:
    query_api = client.query_api()

    now = datetime.utcnow()
    temperature = (
        Point("my_temperature_measurement")
        .tag("location", INFLUX_DB_MEASUREMENT_LOCATION)
        .field("temperature", data['temperature'])
        .time(now, WritePrecision.MS)
    )
    pressure = (
        Point("my_pressure_measurement")
        .tag("location", INFLUX_DB_MEASUREMENT_LOCATION)
        .field("pressure", data['pressure'])
        .time(now, WritePrecision.MS)
    )
    humidity = (
        Point("my_humidity_measurement")
        .tag("location", INFLUX_DB_MEASUREMENT_LOCATION)
        .field("humidity", data['humidity'])
        .time(now, WritePrecision.MS)
    )
    gas_resistance = (
        Point("my_gas_resistance_measurement")
        .tag("location", INFLUX_DB_MEASUREMENT_LOCATION)
        .field("gas_resistance", data['gas_resistance'])
        .time(now, WritePrecision.MS)
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(
        bucket=INFLUX_DB_BUCKET,
        record=[
            temperature,
            pressure,
            humidity,
            gas_resistance
        ],
    )
