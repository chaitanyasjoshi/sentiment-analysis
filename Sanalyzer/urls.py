'''
Created on 01-Dec-2020

@author: Chaitanya Joshi
'''
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Sanalyzer.views import *

urlpatterns = [
    path('Home/', search, name='home'),
    path('Home/search=<str:search>', search, name='home_search'),
    path('Home/index=<int:index>', find_reviews, name='home_reviews'),
] + staticfiles_urlpatterns()