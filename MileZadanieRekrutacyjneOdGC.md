# Task description
The 'https://open-meteo.com/' website provides an open API, that can be used for searching and collecting a detailed weather forecast for a selected location.
There are several measurements to check, including temperature, rain and snowfall, all encoded in the JSON format. The task is to design and code a service that queries for a given location,
collects measurements and logs an alert when thresholds for certain factors are reached.

See `https://open-meteo.com/en/docs` for more insight.

## Requirements
The service must run asynchronously using the producer (alias `WeatherFetcher`) and the consumer (alias `WeatherProcessor`).
The `WeatherFetcher` must query the open-meteo API and be able to pass the collected data to the `WeatherProcessor`.
The `WeatherProcessor` must analyze the received data and print alerts to stdout when:
 - the temperature is below X degrees of Celsius
 - the expected rainfall is greater than Y mm

X and Y should be call command parameters i.e:
```
python main.py -t X -r Y
```

```
       ┌────────────────┐
       │                │
       │   openMeteo    │
       │      API       │
       │                │
       └───────┬────────┘
            ▲  │
            │  │
            │  │2. OpenMeteoAPI data (json)
 1.APIcall  │  │
            │  │
            │  │
┌───────────┼──┼────────────────────────────────────────────────────────┐
│           │  │                                                        │
│           │  │                                                        │
│           │  │                                                        │
│           │  ▼                                                        │
│      ┌────────────┐                               ┌────────────┐      │
│      │            │                               │            │      │
│      │            │ 3. Parsed                     │            │      │
│      │  Weather   │    data ┌──◄────────┐ 3.Parsed│            │      │      ┌──────────────────┐
│      │  Fetcher   │         │           │   data  │ Weather    │  4.Print    │                  │
│      │            ├────────►│           ├────────►│ Processor  │  ────┬─────►│  Output          │
│      │            │         │           │         │            │      │      │                  │
│      │            │         │  Asyncio  │         │            │      │      │      Terminal    │                     
│      │            │         │   Event   │         │            │      │      │                  │          
│      │            │         │   Loop    │         │            │      │      └──────────────────┘
│      │            │         │           │         │            │      │
│      │            │◄────────┤           │◄────────┤            │      │
│      │            │         └────────◄──┘         │            │      │
│      └────────────┘                               └────────────┘      │
│                                                                       │
│                                                                       │
│                                                                       │
│                                                                       │
│                                                                       │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘

     Service
```
Asyncio Event Loop documentation: https://docs.python.org/3/library/asyncio-eventloop.html

### Open-meteo API details
* The example URL for Wrocław looks like that: `https://api.open-meteo.com/v1/forecast?latitude=51.10&longitude=17.03&hourly=temperature_2m,rain`.
* It returns a JSON-encoded document with a bunch of hourly metrics (see `https://jsonformatter.org/json-parser/f7131f`). The indexes in `.hourly.time` column correspond to the indexes in `.hourly.temperature_2m` and `.hourly.rain` columns respectively, i.e `.hourly.time[0]` is the timestamp of the `.hourly.temperature_2m[0]` and `.hourly.rain[0]` measurements, `.hourly.time[1]` corresponds to `.hourly.temperature_2m[1]` and `.hourly.rain[1]`, and so on.

### WeatherFetcher
The `WeatherFetcher`'s role is to:
* Call an open-meteo API (1). 
* Parse the received data and transform them to the in-code representation (2).
* Pass the parsed weather data to the `WeatherProcessor`.

### WeatherProcessor
The `WeatherProcessor`'s role is to:
* Wait for a weather data to come. No interaction back to the `WeatherFetcher` is expected.
* Filter the received weather data and print (to stdout) an alert when the certain thresholds are reached (4).

### Expected outcome
The report should print the timestamp of the forecast along with the detailed values of the measurements.

I.e.
```
---------------------------------REPORT------------------------------------
Warning Wroclaw, low temperature 5.9 of C and rain 0.1 mm expected on 13:00 12-03-2023
Warning Wroclaw, low temperature 5.4 of C and rain 0.1 mm expected on 14:00 12-03-2023
Warning Wroclaw, low temperature 5.0 of C and rain 0.1 mm expected on 15:00 12-03-2023
Warning Wroclaw, low temperature 5.0 of C and rain 0.4 mm expected on 16:00 12-03-2023
Warning Wroclaw, low temperature 5.1 of C and rain 0.4 mm expected on 17:00 12-03-2023
Warning Wroclaw, low temperature 5.4 of C and rain 0.4 mm expected on 18:00 12-03-2023
```

## Constraints
The service must be written in Python. Please use asyncio, json, pytest.
