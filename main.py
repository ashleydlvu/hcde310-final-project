from flask import Flask, render_template, request
import urllib.request, urllib.error, urllib.parse, json, webbrowser
import logging

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



# def safe_get(url):
#     try:
#         return urllib.request.urlopen(url)
#     except urllib.error.HTTPError as e:
#         print("The server couldn't fulfill the request.")
#         print(url)
#         print("Error code: ", e.code)
#     except urllib.error.URLError as e:
#         print("We failed to reach a server")
#         print(url)
#         print("Reason: ", e.reason)
#     return None

# Jinja template
# from jinja2 import Environment, FileSystemLoader
# environment = Environment(loader=FileSystemLoader(""))
# template = environment.get_template("hw6flickrtemplate.html")
# content = template.render(top_views_lst=top_views_lst, top_num_tags_lst=top_num_tags_lst, top_num_comments_lst=top_num_comments_lst)

# with open ("flickr-photos-sorted.html", "w", encoding="utf-8") as f:
#     f.write(content)



# horoscope, what day, data of weather, name
# method to grab horoscope and weather
# ask for name, their sign (display chart for users to see sign)

# s


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


@app.route("/", methods=["GET", "POST"])
def main_handler():
    temp = get_temp()
    app.logger.info("In MainHandler")
    if request.method == 'POST':
        app.logger.info(request.form.get('name'))
        name = request.form.get('username')
        app.logger.info(request.form.get('sign'))
        sign = request.form.get('sign')
        # app.logger.info(request)
        app.logger.info("In POST")
        if name:
        # if form filled in, greet them using this data
            app.logger.info("In NAME")
            return render_template("response.html",
            name=name,
            page_title="Dashboard for %s"%name,
            temp=temp
            )
        else:
        #if not, then show the form again with a correction to the user
            return render_template('form.html',
            page_title="Greeting Form - Error",
            prompt="How can I greet you if you don't enter a name?",
            temp=temp)
    else:
        return render_template('form.html',page_title="Greeting Form", temp=temp)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)