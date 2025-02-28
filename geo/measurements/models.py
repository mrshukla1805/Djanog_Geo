from django.db import models

# Create your models here.


class Measures(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"The distance from {self.location} to {self.destination} is {self.distance} km only."



