from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('showframlist', views.showframlist, name='showframlist'),
    path('predict_dfloc', views.predict_dfloc, name='predict_dfloc'),
    path('getdatarange', views.getdatarange, name='getdatarange'),
    path('upload', views.upload, name='upload'),
]
