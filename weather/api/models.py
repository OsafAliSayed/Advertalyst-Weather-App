from django.db import models

# Create your models here.
class Cities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.id}, {self.name}, {self.country}"