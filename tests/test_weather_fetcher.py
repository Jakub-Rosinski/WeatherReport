import pytest
import WeatherFetcher
import urllib.request

from unittest.mock import MagicMock, patch

mock_meteo_data = {"latitude": 51.1, "longitude": 17.039999, "generationtime_ms": 0.3739595413208008,
                   "utc_offset_seconds": 0,
                   "timezone": "GMT", "timezone_abbreviation": "GMT", "elevation": 118.0,
                   "hourly_units": {"time": "iso8601", "temperature_2m": "°C", "rain": "mm"}, "hourly": {
        "time": ["2023-06-05T00:00", "2023-06-05T01:00", "2023-06-05T02:00", "2023-06-05T03:00", "2023-06-05T04:00",
                 "2023-06-05T05:00", "2023-06-05T06:00", "2023-06-05T07:00", "2023-06-05T08:00", "2023-06-05T09:00",
                 "2023-06-05T10:00", "2023-06-05T11:00", "2023-06-05T12:00", "2023-06-05T13:00", "2023-06-05T14:00",
                 "2023-06-05T15:00", "2023-06-05T16:00", "2023-06-05T17:00", "2023-06-05T18:00", "2023-06-05T19:00",
                 "2023-06-05T20:00", "2023-06-05T21:00", "2023-06-05T22:00", "2023-06-05T23:00", "2023-06-06T00:00",
                 "2023-06-06T01:00", "2023-06-06T02:00", "2023-06-06T03:00", "2023-06-06T04:00", "2023-06-06T05:00",
                 "2023-06-06T06:00", "2023-06-06T07:00", "2023-06-06T08:00", "2023-06-06T09:00", "2023-06-06T10:00",
                 "2023-06-06T11:00", "2023-06-06T12:00", "2023-06-06T13:00", "2023-06-06T14:00", "2023-06-06T15:00",
                 "2023-06-06T16:00", "2023-06-06T17:00", "2023-06-06T18:00", "2023-06-06T19:00", "2023-06-06T20:00",
                 "2023-06-06T21:00", "2023-06-06T22:00", "2023-06-06T23:00", "2023-06-07T00:00", "2023-06-07T01:00",
                 "2023-06-07T02:00", "2023-06-07T03:00", "2023-06-07T04:00", "2023-06-07T05:00", "2023-06-07T06:00",
                 "2023-06-07T07:00", "2023-06-07T08:00", "2023-06-07T09:00", "2023-06-07T10:00", "2023-06-07T11:00",
                 "2023-06-07T12:00", "2023-06-07T13:00", "2023-06-07T14:00", "2023-06-07T15:00", "2023-06-07T16:00",
                 "2023-06-07T17:00", "2023-06-07T18:00", "2023-06-07T19:00", "2023-06-07T20:00", "2023-06-07T21:00",
                 "2023-06-07T22:00", "2023-06-07T23:00", "2023-06-08T00:00", "2023-06-08T01:00", "2023-06-08T02:00",
                 "2023-06-08T03:00", "2023-06-08T04:00", "2023-06-08T05:00", "2023-06-08T06:00", "2023-06-08T07:00",
                 "2023-06-08T08:00", "2023-06-08T09:00", "2023-06-08T10:00", "2023-06-08T11:00", "2023-06-08T12:00",
                 "2023-06-08T13:00", "2023-06-08T14:00", "2023-06-08T15:00", "2023-06-08T16:00", "2023-06-08T17:00",
                 "2023-06-08T18:00", "2023-06-08T19:00", "2023-06-08T20:00", "2023-06-08T21:00", "2023-06-08T22:00",
                 "2023-06-08T23:00", "2023-06-09T00:00", "2023-06-09T01:00", "2023-06-09T02:00", "2023-06-09T03:00",
                 "2023-06-09T04:00", "2023-06-09T05:00", "2023-06-09T06:00", "2023-06-09T07:00", "2023-06-09T08:00",
                 "2023-06-09T09:00", "2023-06-09T10:00", "2023-06-09T11:00", "2023-06-09T12:00", "2023-06-09T13:00",
                 "2023-06-09T14:00", "2023-06-09T15:00", "2023-06-09T16:00", "2023-06-09T17:00", "2023-06-09T18:00",
                 "2023-06-09T19:00", "2023-06-09T20:00", "2023-06-09T21:00", "2023-06-09T22:00", "2023-06-09T23:00",
                 "2023-06-10T00:00", "2023-06-10T01:00", "2023-06-10T02:00", "2023-06-10T03:00", "2023-06-10T04:00",
                 "2023-06-10T05:00", "2023-06-10T06:00", "2023-06-10T07:00", "2023-06-10T08:00", "2023-06-10T09:00",
                 "2023-06-10T10:00", "2023-06-10T11:00", "2023-06-10T12:00", "2023-06-10T13:00", "2023-06-10T14:00",
                 "2023-06-10T15:00", "2023-06-10T16:00", "2023-06-10T17:00", "2023-06-10T18:00", "2023-06-10T19:00",
                 "2023-06-10T20:00", "2023-06-10T21:00", "2023-06-10T22:00", "2023-06-10T23:00", "2023-06-11T00:00",
                 "2023-06-11T01:00", "2023-06-11T02:00", "2023-06-11T03:00", "2023-06-11T04:00", "2023-06-11T05:00",
                 "2023-06-11T06:00", "2023-06-11T07:00", "2023-06-11T08:00", "2023-06-11T09:00", "2023-06-11T10:00",
                 "2023-06-11T11:00", "2023-06-11T12:00", "2023-06-11T13:00", "2023-06-11T14:00", "2023-06-11T15:00",
                 "2023-06-11T16:00", "2023-06-11T17:00", "2023-06-11T18:00", "2023-06-11T19:00", "2023-06-11T20:00",
                 "2023-06-11T21:00", "2023-06-11T22:00", "2023-06-11T23:00"],
        "temperature_2m": [12.1, 11.5, 10.7, 9.6, 10.2, 11.9, 14.5, 17.2, 19.7, 22.0, 23.3, 24.0, 24.6, 25.0, 25.2,
                           24.6, 24.3, 23.5, 22.1, 20.5, 19.1, 18.1, 17.5, 17.0, 16.1, 15.6, 15.1, 14.8, 14.6, 15.0,
                           15.9, 17.1, 18.8, 20.4, 21.9, 23.5, 24.9, 25.9, 25.7, 25.3, 23.9, 23.3, 22.3, 20.5, 18.8,
                           17.8, 16.7, 15.8, 15.1, 14.7, 14.2, 13.7, 13.8, 15.4, 16.9, 17.8, 18.3, 20.0, 21.6, 23.0,
                           24.2, 24.2, 24.0, 23.7, 23.3, 21.7, 21.3, 20.4, 19.6, 18.7, 17.9, 17.3, 17.0, 16.6, 16.2,
                           15.7, 15.7, 16.7, 18.3, 19.7, 21.2, 22.5, 23.1, 23.9, 24.4, 24.3, 23.9, 23.4, 23.0, 22.5,
                           21.7, 20.6, 19.3, 18.2, 17.6, 17.2, 16.9, 16.7, 16.5, 16.6, 17.0, 17.5, 18.3, 19.4, 20.7,
                           21.7, 22.3, 22.6, 22.7, 22.4, 22.0, 21.4, 20.8, 20.2, 19.5, 19.0, 18.5, 18.0, 17.6, 17.3,
                           17.0, 16.7, 16.5, 16.5, 16.8, 17.3, 17.6, 19.0, 20.0, 20.9, 21.7, 22.4, 22.9, 23.2, 23.2,
                           23.0, 22.4, 21.5, 20.6, 19.7, 18.8, 18.0, 17.5, 17.1, 16.7, 16.4, 16.1, 16.1, 16.4, 16.9,
                           17.5, 18.3, 19.3, 20.2, 21.0, 21.7, 22.2, 22.3, 22.1, 21.7, 21.0, 20.1, 19.2, 18.6, 18.0,
                           17.5, 17.4, 17.3],
        "rain": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.00, 0.10, 0.10, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]}}


@pytest.fixture()
def mock_geopy(mocker):
    mock = MagicMock(return_value=(0.0, 0.0))
    mocker.patch("WeatherFetcher.location_to_coords", return_value=mock)
    return mock


def test_location_to_coords(mock_geopy):
    coords = WeatherFetcher.location_to_coords("test").return_value
    latitude, longitude = coords[0], coords[1]
    assert latitude == 0.0
    assert longitude == 0.0


@patch("WeatherFetcher.location_to_coords", return_value=(0.0, 0.0))
def test_prepare_url(_):
    prepare_url = WeatherFetcher.prepare_url("test")
    assert prepare_url == "https://api.open-meteo.com/v1/forecast?latitude=0.0&longitude=0.0&hourly=temperature_2m,rain"


@patch('urllib.request.urlopen')
def test_get_meteo_data(mock_urlopen):
    cm = MagicMock()
    cm.getcode.return_value = 200
    cm.read.return_value = 'contents'
    cm.__enter__.return_value = cm
    mock_urlopen.return_value = cm

    with urllib.request.urlopen('http://foo') as response:
        assert response.getcode() == 200
        assert response.read() == 'contents'


@patch("WeatherFetcher.get_meteo_data", return_value=mock_meteo_data)
def test_get_data(get_meteo_data):
    assert "location" in WeatherFetcher.get_data("test")
