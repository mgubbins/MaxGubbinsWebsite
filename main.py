# import flask
import calendar
import datetime
import requests
from flask import Flask, render_template, url_for

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# create instance of flask web application
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/resume")
def resume():
    return render_template("resume.html")


# defining homepage function that will run on website
@app.route("/localClimbingWeather")  # defining how to access page.
def home():

        # Muscatatuck
        area1var = 'Muscatatuck<br>'
        report = weather(38.98, -85.62)
        for i in report:
            area1var += i + "</br>"

        area2var = '<br>Unlikely Wall<br>'
        report = weather(39.02, -86.54)
        for i in report:
            area2var += i + "</br>"

        area3var = '<br>Jackson Falls<br>'
        report = weather(37.51, -88.69)
        for i in report:
            area3var += i + "</br>"

        area4var = '<br>Holy Boulders<br>'
        report = weather(37.62, -89.42)
        for i in report:
            area4var += i + "</br>"

        area5var = '<br>Red River Gorge<br>'
        report = weather(37.46, -83.79)
        for i in report:
            area5var += i + "</br>"
        return render_template("localWeather.html", area1=area1var, area2=area2var, area3=area3var, area4=area4var, area5=area5var)


def weather(lat, lon):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid=4932b25fcb6ea02e1c6e7c28b2d98178')
    resJson = res.json()

    report = []
    counter = 0

    daily = resJson["daily"]
    for i in daily:
        weekday = datetime.datetime.fromtimestamp(daily[counter]["dt"]).weekday()
        morningtemp = str(ktof(daily[counter]["temp"]["morn"]))
        afternoontemp = str(ktof(daily[counter]["temp"]["day"]))
        eveningtemp = str(ktof(daily[counter]["temp"]["eve"]))
        humidity = str(daily[counter]["humidity"])
        description = daily[counter]["weather"][0]["description"]

        report.append(calendar.day_name[
                          weekday] + ": " + "Morn: " + morningtemp + " Day: " + afternoontemp + " Eve: " + eveningtemp + " Humidity: " + humidity + "% Conditions: " + description + "<br>")
        counter += 1
    dt = datetime.datetime.fromtimestamp(daily[0]["dt"]).strftime("%m/%d/%Y")

    temp = res.text

    return report


def ktof(kelvin):
    fahrenheit = (kelvin - 273.15) * (9 / 5) + 32
    return int(fahrenheit)


# run app
if __name__ == "__main__":
    app.run()
