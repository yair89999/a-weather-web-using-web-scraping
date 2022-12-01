from flask import Flask,redirect,url_for, render_template, request, session, flash
import os,requests
from bs4 import BeautifulSoup
from datetime import datetime
app = Flask(__name__)

def get_weather(city2):
    try:
        if len(city2.split(" ")) > 1: # more then just one word
            city = "+".join(city2.split(" "))
        else: city = city2
        url = f"https://www.google.com/search?q=weather+in+{city}&oq=tel&aqs=chrome.0.69i59j69i57j0i433i512l2j46i433i512j0i433i512j46i512j0i433i512j0i131i433i512j0i433i512.720j0j7&sourceid=chrome&ie=UTF-8"
        result = requests.get(url).text
        docs = BeautifulSoup(result, "html.parser") # gets the text/parse the text

        weather = docs.find_all("span", dir="ltr", limit=1)[0].string
        print(f"the weather in {city2} is: "+weather)

        # get fahrenheit
        fahrenheit_weather = weather
        new_temp = ""
        for num in fahrenheit_weather:
            try: 
                int(num)
                new_temp+=num
            except:pass
        new_temp = str(int(new_temp)*1.8 +32)
        new_temp += "°F"
        print(f"the weather in {city2} is: "+new_temp)

        # get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return f"the weather in {city2} is: "+weather +", "+ new_temp + f"\nfor the time of: {current_time}"

    except: return "couldn't find the weather, check if the city/country name is correct"


@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        place = request.form["place"]
        print("user searched: "+place)
        weather2 = get_weather(place)
        print(weather2)
        return render_template("show_weather.html", weather = weather2)
    return render_template("collect_place.html")

if __name__ == "__main__":
    app.run(debug=True)