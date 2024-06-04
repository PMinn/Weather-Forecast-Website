from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from . import env
import requests
from datetime import datetime, timezone, timedelta, date
import math
from django.contrib.auth.models import User
from user.models import UserProfile
from .counties import counties

weekdayNames = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        userProfile, _ = UserProfile.objects.get_or_create(user=user)
        return redirect(f'/county/details/{userProfile.defaultCounty}')
    return render(request, 'index.html', {'counties': counties})


class WeatherForecast:
    def __init__(self, i):
        self.Wx = ""
        self.MaxT = -999
        self.MinT = 999
        if i == 0:
            self.weekday = "今天"
        if i == 1:
            self.weekday = "明天"
        elif i == 2:
            self.weekday = "後天"
        else:
            self.weekday = weekdayNames[(
                date.today() + timedelta(days=i)).weekday()]

    def updateWx(self, Wx):
        self.Wx = Wx
        if '雲' in self.Wx or '陰' in self.Wx:
            self.weatherIcon = "cloudy"
            if ('電' in self.Wx or '雷' in self.Wx) and '雨' in self.Wx:
                self.weatherIcon = "cloud-lightning-rain"
            elif '雨' in self.Wx and '雪' in self.Wx:
                self.weatherIcon = "cloud-sleet"
            elif '雪' in self.Wx:
                self.weatherIcon = "cloud-snow"
            elif '霧' in self.Wx:
                self.weatherIcon = "cloud-fog"
            elif '冰' in self.Wx or '雹' in self.Wx:
                self.weatherIcon = "cloud-hail"
            elif '霾' in self.Wx:
                self.weatherIcon = "cloud-haze"
            elif '電' in self.Wx or '雷' in self.Wx:
                self.weatherIcon = "cloud-lightning"
            elif '雨' in self.Wx:
                self.weatherIcon = "cloud-rain"
        else:
            self.weatherIcon = "sun"
            if '電' in self.Wx or '雷' in self.Wx:
                self.weatherIcon = "lightning"
            elif '雪' in self.Wx:
                self.weatherIcon = "snow"

    def updateMaxT(self, MaxT):
        if MaxT > self.MaxT:
            self.MaxT = MaxT

    def updateMinT(self, MinT):
        if MinT < self.MinT:
            self.MinT = MinT


def weatherDataProcessing(data):
    # add AT
    T = data['AirTemperature']
    E = (data['RelativeHumidity']/100) * 6.105 * \
        math.exp((T * 17.27) / (T + 237.7))
    AT = 1.07 * T + 0.2 * E - 0.65 * data['WindSpeed'] - 2.7
    data['AT'] = round(AT * 10) / 10
    # add UVString
    if data['UVIndex'] < 0:
        data['UVString'] = "資料異常"
    if data['UVIndex'] < 3:
        data['UVString'] = "低量級"
    elif data['UVIndex'] < 6:
        data['UVString'] = "中量級"
    elif data['UVIndex'] < 8:
        data['UVString'] = "高量級"
    elif data['UVIndex'] < 11:
        data['UVString'] = "過量級"
    else:
        data['UVString'] = "危險級"
    return data


def county_details(request, county):
    isSuccess = False
    template = loader.get_template('county\details\[county].html')
    result = requests.get(
        f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-005?Authorization={env.cwa_apikey}&downloadType=WEB&format=JSON")
    json = result.json()
    data = {
        "pageCounty": county,
        "weatherForecast": [WeatherForecast(i) for i in range(7)],
        "counties": map(lambda x: x['locationName'], json['cwaopendata']['dataset']['location'])
    }
    if request.user.is_authenticated:
        data['userProfile'], _ = UserProfile.objects.get_or_create(
            user=request.user)
    for location in json['cwaopendata']['dataset']['location']:
        if location['locationName'] == county:
            weatherElement = location['weatherElement']
            for element in weatherElement:
                for time in element['time']:
                    startTime = datetime.fromisoformat(time['startTime'])
                    now = datetime.now(timezone.utc)
                    delta = startTime - now
                    deltaDays = delta.days
                    index = 0
                    if deltaDays >= 0 and deltaDays <= 6:
                        index = deltaDays
                    if element['elementName'] == 'Wx':
                        data['weatherForecast'][index].updateWx(
                            time['parameter']['parameterName'])
                    elif element['elementName'] == 'MaxT':
                        data['weatherForecast'][index].updateMaxT(
                            int(time['parameter']['parameterName']))
                    elif element['elementName'] == 'MinT':
                        data['weatherForecast'][index].updateMinT(
                            int(time['parameter']['parameterName']))
            isSuccess = True
    if isSuccess:
        isSuccess = False
        result = requests.get(
            f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization={env.cwa_apikey}&format=JSON")
        json = result.json()
        if json['success'] == 'true':
            for station in json['records']['Station']:
                if (station['GeoInfo']['CountyName'] == county):
                    weatherElement = station['WeatherElement']
                    data['weather'] = weatherDataProcessing(weatherElement)
                    isSuccess = True
                    return HttpResponse(template.render(data, request))
    return HttpResponseNotFound(loader.get_template('404.html').render())
