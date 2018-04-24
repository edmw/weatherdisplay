# coding: utf-8

# 8. Data Types
import collections

# 3rd Party Libraries
from influxdb import InfluxDBClient


Weather = collections.namedtuple("Weather", [
    "outdoor_temperature",
    "outdoor_humidity",
    "outdoor_pressure",
    "indoor_temperature",
    "indoor_humidity",
    "indoor_pressure",
])

Measurement = collections.namedtuple("Measurement", [
    "name",
    "value",
    "time",
])


class Reader:

    def __init__(self, db, host, port):
        self.db = InfluxDBClient(host=host, port=port, database=db)

    def get_last(self, key, location):
        results = self.db.query(
            "SELECT LAST(\"{}\") "
            "FROM \"weather\" "
            "WHERE \"location\" = '{}'".format(key, location)
        )
        point = next(results.get_points(), None)
        return Measurement(
            key,
            point["last"] if point else None,
            point["time"] if point else None,
        )

    def read(self):
        return Weather(
            self.get_last("temperature1", "terrace"),
            self.get_last("humidity0", "terrace"),
            self.get_last("pressure0", "terrace"),
            self.get_last("temperature0", "indoor"),
            self.get_last("humidity0", "indoor"),
            self.get_last("pressure0", "indoor"),
        )
