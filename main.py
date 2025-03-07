from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_KEY = "06f2727175b96cbab17fbf3e4f71d40d"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.form.get("city")

    
    if not city or not validate_city_name(city):
        return render_template("index.html", error="Please enter a valid city name!")

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" 
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
        return render_template("index.html", weather=weather)
    elif response.status_code == 404:
        return render_template("index.html", error="City not found! Please check the name.")
    else:
        return render_template("index.html", error="Unable to fetch weather data at the moment. Please try again later.")

def validate_city_name(city):
    """
    Validates the city name input.
    Allows alphabetic characters and spaces.
    """
    return all(part.isalpha() for part in city.split()) and len(city) > 1

if __name__ == "__main__":
    app.run(debug=True)
