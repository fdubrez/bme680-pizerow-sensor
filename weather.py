import argparse, os, requests
from datetime import datetime
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


parser = argparse.ArgumentParser(description="Retrieve weather for coordinates using openweather API & store it in InfluxDB")
parser.add_argument("-lat", "--latitude")
parser.add_argument("-long", "--longitude")
parser.add_argument('-s', '--store', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

# Retrieve weather data
OPENWEATHER_APPID=os.getenv("OPENWEATHER_APPID")
response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={args.latitude}&lon={args.longitude}&appid={OPENWEATHER_APPID}&units=metric")
if response.status_code != 200:
    raise Exception(f"Failed to retrieve weather data, status_code={response.status_code} response={response.text}")
data = response.json()
temperature = data["main"]["temp"]
print(f"temperature is {temperature}")

if args.store is False:
    exit(0)

# InfluxDB env
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
        .field("temperature", temperature)
        .time(now, WritePrecision.MS)
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(
        bucket=INFLUX_DB_BUCKET,
        record=[
            temperature
        ],
    )