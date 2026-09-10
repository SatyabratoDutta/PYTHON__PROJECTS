import tkinter as tk
from tkinter import messagebox
import requests

weather_codes = {
    0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Fog", 48: "Fog", 51: "Light Drizzle", 53: "Moderate Drizzle",
    55: "Heavy Drizzle", 61: "Light Rain", 63: "Moderate Rain",
    65: "Heavy Rain", 71: "Light Snow", 73: "Moderate Snow",
    75: "Heavy Snow", 80: "Rain Showers", 81: "Rain Showers",
    82: "Heavy Rain Showers", 95: "Thunderstorm"
}

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Enter a city name")
        return

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
        geo_data = requests.get(geo_url, params=geo_params, timeout=10).json()

        if "results" not in geo_data:
            messagebox.showerror("Error", "City not found")
            return

        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "timezone": "auto"
        }

        current = requests.get(weather_url, params=weather_params, timeout=10).json()["current"]

        result_label.config(text=(
            f"📍 {city_name}, {country}\n\n"
            f"🌡 Temperature: {current['temperature_2m']} °C\n\n"
            f"🤗 Feels Like: {current['apparent_temperature']} °C\n\n"
            f"💧 Humidity: {current['relative_humidity_2m']}%\n\n"
            f"💨 Wind Speed: {current['wind_speed_10m']} km/h\n\n"
            f"☁ Condition: {weather_codes.get(current['weather_code'], 'Unknown')}"
        ))

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Check your internet connection")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("450x550")
root.resizable(False, False)

tk.Label(root, text="🌦 Weather Dashboard", font=("Arial", 24, "bold")).pack(pady=25)
tk.Label(root, text="Enter City Name", font=("Arial", 13)).pack()

city_entry = tk.Entry(root, font=("Arial", 16), width=25, justify="center")
city_entry.pack(pady=15)

tk.Button(
    root, text="🔍 Get Weather", font=("Arial", 13, "bold"),
    command=get_weather
).pack(pady=10)

result_label = tk.Label(
    root, text="Enter a city to see weather",
    font=("Arial", 13), justify="left"
)
result_label.pack(pady=30)

tk.Label(
    root, text="Powered by Open-Meteo", font=("Arial", 9)
).pack(side="bottom", pady=15)

root.mainloop()
