import asyncio
import argparse

from WeatherFetcher import get_data
from WeatherProcessor import AnalyzeWeatherData

DEFAULT_LOCATION = "Gliwice"


def parse_args():
    args = argparse.ArgumentParser(description="""Service for fetching data from Open-Meteo API""")
    args.add_argument("-t",
                      "--temperature",
                      required=True,
                      type=float)
    args.add_argument("-r",
                      "--rainfall",
                      required=True,
                      type=float)
    args.add_argument("-l",
                      "--location",
                      type=str,
                      default=DEFAULT_LOCATION)
    return args.parse_args()


if __name__ == '__main__':
    args = parse_args()
    data = get_data(args.location)
    if data:
        if args.location == DEFAULT_LOCATION:
            print(f"No location provided, displaying data for default location: {DEFAULT_LOCATION}")
        if args.rainfall < 0.0:
            print(f"Rainfall must be greater than zero - value provided: {args.rainfall}")
            exit(2)
        a = AnalyzeWeatherData(data, args.temperature, args.rainfall)
        loop = asyncio.new_event_loop()
        try:
            print(" --------------------------------------  REPORT  ----------------------------------------- ")
            loop.run_until_complete(a.analyze())
        finally:
            loop.close()
            exit(0)
    else:
        print("No data Retrieved")
        exit(1)
