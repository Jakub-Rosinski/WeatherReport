import dataclasses

from dateutil import parser


@dataclasses.dataclass
class AnalyzeWeatherData:
    data: dict
    t_limit: float
    r_limit: float

    def get_hourly_data(self) -> tuple:
        hourly_data = self.data["hourly"]
        return hourly_data["time"], hourly_data["temperature_2m"], hourly_data["rain"]

    def get_hourly_units(self, unit_for: str) -> str:
        data = self.data["hourly_units"]
        return data.get(unit_for)

    async def analyze(self) -> bool:
        location = self.data["location"]
        time, temperature, rain = self.get_hourly_data()
        for t, tm, r in zip(time, temperature, rain):
            if tm < self.t_limit and r >= self.r_limit:
                print(f"Warning for {location} - low temperature: {tm}{self.get_hourly_units('temperature_2m')} "
                      f"and rain {r}{self.get_hourly_units('rain')} expected on {parser.parse(t)}")
        return True
