import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=30)

    def __str__(self):
        return self.city_name


class Temperature(models.Model):
    date = models.DateTimeField()
    temperature = models.IntegerField()
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city_name}: {self.temperature}'

    def was_find_recently(self):
        return self.date >= (timezone.now() - datetime.timedelta(days=7))

    # def was_find_now(self):
    #     return self.date >= (timezone.now() - datetime.timedelta(minutes=1))

'''
from django.utils import timezone
from weather.models import City, Temperature
c = City.objects.get(id = 1)
c.temperature_set.all()
'''