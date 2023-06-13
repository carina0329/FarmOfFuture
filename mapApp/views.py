from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from insert_image import *
from insert_data import *
import json
from mapApp.models import Satellite, Sensor
from mapApp.serializer import SatelliteSerializer, SensorSerializer

# Create your views here.
@csrf_exempt
def SensorDataAPI(request):
    # if the request type is get, we would render all data as json objects
    if request.method == 'GET':
        sensorDataObj = Sensor.objects.all()
        sensorDataSerializer = SensorSerializer(sensorDataObj, many=True)
        return JsonResponse(sensorDataSerializer.data, safe=False)

@csrf_exempt
def SensorGetLastTen(request):
    # if the request type is get, we would render all data as json objects
    if request.method == 'GET':
        res_lst = get_last_10_days()
        res_lst_json = json.dumps(res_lst)
        return JsonResponse(res_lst_json, safe=False)

@csrf_exempt
def SatelliteDataAPI(request, date=''):
    # if the request type is get, we would render all data as json objects
    if request.method == 'GET':
        # satelliteImageDataObj = Satellite.objects.get(RasterFileName = rasterFileName)
        resJsonObjectStr = read_image_data(date)
        return HttpResponse(resJsonObjectStr)
    
    if request.method == 'POST':
        responseString = "The data on " + date + " has been successfully inserted \n"
        insert_data_all(date)
        return HttpResponse(responseString)
@csrf_exempt
def SatelliteGetDate(request):
    if request.method == 'GET':
        responseString = str(get_satellite_available_dates())
        return HttpResponse(responseString)