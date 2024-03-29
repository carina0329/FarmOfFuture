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
from planet_api_requests import *

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
def PlanetImageAPI(request, date=''):
    responseString = ""
    if request.method == 'GET':
        planetRequests = PlanetRequests()
        item_ids = planetRequests.search(date)
        if(len(item_ids) > 0):
            try:
                order_id = planetRequests.place_order(item_ids, "Images_on_{}".format(date))
                planetRequests.download_order(order_id, "images_{}".format(date))
                responseString = "Order with id {} has been downloaded successfully in {}".format(order_id, "images_{}".format(date))
            except Exception as error:
                responseString = "Error {} encountered during placing or downloading order!".format(error)
            finally:
                return HttpResponse(responseString)
        responseString = "No results were found in the search. Try different filters and search again"
        return HttpResponse(responseString)

@csrf_exempt
def SatelliteGetDate(request):
    if request.method == 'GET':
        responseString = str(get_satellite_available_dates())
        return HttpResponse(responseString)