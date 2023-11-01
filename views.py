from django.shortcuts import render
from django.http import HttpResponse
import requests
import pickle
import numpy as np


# Create your views here.

def index(request):
    lang = request.GET.get('long', '')
    lat = request.GET.get('lat', '')
    # return HttpResponse("<h1>Welcome to Django</h1><h3>Long = {} and lat={}".format(long,lat))
    # p1={"lat":39.1813855,"lon":-77.1827295}

    p1 = {"lat": lat, "lon": lang}

    rest_url = "https://rest.isric.org"
    prop_query_url = f"{rest_url}/soilgrids/v2.0/properties/query"

    props = {"property": "silt", "depth": "0-5cm", "value": "mean"}
    res1 = requests.get(prop_query_url, params={**p1, **props})
    res = res1.json()['properties']["layers"][0]["depths"][0]["values"]
    silt = res["mean"] / 10

    props = {"property": "sand", "depth": "0-5cm", "value": "mean"}
    res1 = requests.get(prop_query_url, params={**p1, **props})
    res = res1.json()['properties']["layers"][0]["depths"][0]["values"]
    sand = res["mean"] / 10

    props = {"property": "phh2o", "depth": "0-5cm", "value": "mean"}
    res1 = requests.get(prop_query_url, params={**p1, **props})
    res = res1.json()['properties']["layers"][0]["depths"][0]["values"]
    ph = res["mean"] / 10

    props = {"property": "clay", "depth": "0-5cm", "value": "mean"}
    res1 = requests.get(prop_query_url, params={**p1, **props})
    res = res1.json()['properties']["layers"][0]["depths"][0]["values"]
    clay = res["mean"] / 10

    props = {"property": "nitrogen", "depth": "0-5cm", "value": "mean"}
    res1 = requests.get(prop_query_url, params={**p1, **props})
    res = res1.json()['properties']["layers"][0]["depths"][0]["values"]
    nitrogen = res["mean"] / 10

    data = np.array([[ph, sand, silt, clay, nitrogen]])

    file = open("E:\\Project work  2021\\crops\\demo\\Knn.pkl", 'rb')
    object_file = pickle.load(file)
    prediction = object_file.predict(data)
    print(prediction[0])
    d = {"silt": silt, "sand": sand, "ph": ph, "clay": clay, "nitrogen": nitrogen, "lang": lang, "lat": lat,
         "crop": prediction[0]}
    return render(request, "demo/index.html", {'dict': d})


def greet(request, name):
    return HttpResponse("<h2>You hsave selected greet function</h2><br>The parater is {}".format(name))


def fact(request, value):
    fact = 1
    for i in range(1, value + 1):
        fact = fact * i

    return HttpResponse("<h3><font color=red>Factorial of {} = {}".format(value, fact))
