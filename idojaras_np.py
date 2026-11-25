import requests

class IdojarasKezeloNP:
    def __init__(self):
        self.munkamenet = requests.Session()
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.ido_url = "https://api.open-meteo.com/v1/forecast"

    def hely_kereses(self, varos_nev):
        kodolt_nev = requests.utils.quote(varos_nev)
        parameterek = {
            "name": varos_nev,
            "count": 10,
            "language": "hu",
            "format": "json"
        }
        try:
            valasz = self.munkamenet.get(
                self.geo_url,
                params=parameterek,
                timeout=10
            )
            valasz.raise_for_status()
            adatok = valasz.json()
        except requests.RequestException:
            return None

        for elem in adatok.get("results", []):
            if elem.get("country_code") == "HU":
                return (
                    elem.get("name"),
                    elem.get("admin1", "Ismeretlen vármegye"),
                    elem.get("latitude"),
                    elem.get("longitude"),
                    kodolt_nev
                )
        return None


def idojaras_adat_lekeres_np(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    parameterek = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,wind_speed_10m"
        ),
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Budapest",
        "forecast_days": 3
    }
    try:
        valasz = requests.get(url, params=parameterek, timeout=10)
        valasz.raise_for_status()
        return valasz.json()
    except requests.RequestException:
        return None