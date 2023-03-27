from django.db import models

# Create your models here.
class Satellite(models.Model):
    # this is get directly from planet API
    RasterFileName = models.CharField(max_length=200)
    RasterFilePath = models.CharField(max_length=500, primary_key = True)
    ImageFileName = models.CharField(max_length=200)
    ImageFilePath = models.CharField(max_length=500, default = "")
    ImageFileBlob = models.TextField(blank=True)
    Date = models.DateField()
    TopleftLat = models.FloatField(max_length=200)
    TopleftLng = models.FloatField(max_length=200)
    ToprightLat = models.FloatField(max_length=200)
    ToprightLng = models.FloatField(max_length=200)
    BottomleftLat = models.FloatField(max_length=200)
    BottomleftLng = models.FloatField(max_length=200)

    
# "Date","Depth","Site","Plot","Year","Value"
class Sensor(models.Model):
    Stream_id = models.AutoField(primary_key=True, default = 0)
    Date = models.DateField()
    Depth = models.IntegerField()
    Site = models.CharField(max_length=500)
    Plot = models.CharField(max_length=200)
    Year = models.IntegerField()
    Value = models.FloatField(max_length=200)
    # id = CompositeKey(columns=['Date', 'Depth', 'Site'])
    class Meta:
        unique_together = ('Date', 'Depth', 'Site',)