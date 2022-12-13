from flask import Flask, render_template, request
import urllib.request, urllib.error, urllib.parse, json, webbrowser, requests, pyaztro
import logging
from datetime import datetime

app = Flask(__name__)


def get_temp():
    lat = 47.653456
    lng = -122.307544

    locurl = "https://api.weather.gov/points/{lat},{lng}".format(lat=lat,lng=lng) 
    result = nws_get(locurl)

    if result is not None: 
        locdata = json.load(result)
        # print(pretty(locdata))
        # third - use that info to fill in this URL and ask for the forecast:
        # https://api.weather.gov/gridpoints{office}/{grid X},{grid y}/forecast
        # I'll need to deal with authentication here.
        hourly_forecast_url = locdata['properties']['forecastHourly']
        hourly_forecast_url = locdata['properties']['forecastHourly']
        hourly_forecast_result = nws_get(hourly_forecast_url)
        hourly_forecast_json = json.load(hourly_forecast_result)
        temp = hourly_forecast_json["properties"]["periods"][0]["temperature"]
        # third - use that info to fill in this URL and ask for the forecast:
        # https://api.weather.gov/gridpoints{office}/{grid X},{grid y}/forecast
        return temp

#def userInput():

def get_horoscope(sign):
    horoscope = pyaztro.Aztro(sign=sign) #sign = userInput
    # print(horoscope.mood)
    # print(horoscope.lucky_time)
    # print(horoscope.description)
    # print(horoscope.date_range)
    # print(horoscope.color)
    # print(horoscope.compatibility)
    return horoscope
    #posts return info

get_horoscope("capricorn")


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)
# Docs: https://www.weather.gov/documentation/services-web-api
def nws_get(url):
# make a request with the url and necessary headers
    # User-Agent: (myweatherapp.com, contact@myweatherapp.com)
    headers = {"User-Agent":"Ashley Vu, ashleyvu@uw.edu"}
    req = urllib.request.Request(url, headers=headers)
    # then pass that request to safe_get
    return safe_get(req)

def timeConvert(miliTime):
    hours, minutes = miliTime.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "AM"
    if hours > 12:
        setting = "PM"
        hours -= 12
    return hours,minutes,setting


@app.route("/", methods=["GET", "POST"])
def main_handler():
    now = datetime.now()
    time = now.strftime("%H:%M")
    hours,minutes,setting = timeConvert(time)
    time = str(hours) + ":{:02d}".format(minutes) + " " + setting
    temp = get_temp()
    if request.method == 'POST':
        name = request.form.get('name')
        sign = request.form.get('sign')
        # app.logger.info(request)
        if name and sign:
        # if form filled in, greet them using this data
            try:
                horoscope = get_horoscope(sign)
            except pyaztro.exceptions.PyAztroSignException as e:
                return render_template('form.html',
                page_title="Horoscope Form - Error",
                prompt="Oops! We didn't recognize that sign, please check your spelling to input a valid astrology sign.",
                temp=temp,
                time=time)
            return render_template("response.html",
            name=name,
            page_title="Dashboard for %s"%name,
            temp=temp,
            time=time,
            horoscope=horoscope
            )
        else:
        #if not, then show the form again with a correction to the user
            return render_template('form.html',
            page_title="Horoscope Form - Error",
            prompt="Please enter your name and horoscope so we can show you your lucky signs for the day :)",
            temp=temp,
            time=time)
    else:
        return render_template('form.html',page_title="Greeting Form", temp=temp, time=time)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)