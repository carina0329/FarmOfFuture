from django.urls import re_path
from mapApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^viewsensordata$', views.SensorDataAPI),
    re_path(r'^viewsatellitedata/(.*?)$', views.SatelliteDataAPI),
    re_path(r'^insertsatellitedata/(.*?)$', views.SatelliteDataAPI),
    re_path(r'^getavailabledate/$', views.SatelliteGetDate),
    re_path(r'^getlast10/$', views.SensorGetLastTen),
    re_path(r'^getsatellitedata/(.*?)$', views.PlanetImageAPI)
]
