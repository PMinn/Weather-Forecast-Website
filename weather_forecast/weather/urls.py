from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('county/details/<str:county>',
         views.county_details, name='county_details'),
]
