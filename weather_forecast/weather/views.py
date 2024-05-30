from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from . import env
import requests



def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def county_details(request, county):
    template = loader.get_template('county\details\[county].html')
    result = requests.get(
        f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-005?Authorization={env.cwa_apikey}&downloadType=WEB&format=JSON")
    json = result.json()
    for data in json['cwaopendata']['dataset']['location']:
        print(data['locationName'])
        print(data['locationName'] == county)
        if data['locationName'] == county:
            return HttpResponse(template.render(data, request))
    raise ValueError('County not found')
