from rest_framework import serializers
from mapApp.models import Satellite, Sensor

class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = ['RasterFileName', 'ImageFileName', 'ImageFileBlob']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['Stream_id', 'Date', 'Depth', 'Site', 'Plot', 'Year', 'Value']