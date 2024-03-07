from django.db import models

# Create your models here.
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.id}, {self.name}, {self.country}"
    
class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    condition = models.CharField(max_length=255)
    icon_url = models.CharField(max_length=500)
    
    