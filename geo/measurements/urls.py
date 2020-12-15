from django.urls import path
from .views import cal_distance

app_name = 'measurements'

urlpatterns = [
    path('',cal_distance,name='cal_dist'),
]