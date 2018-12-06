from django.conf.urls import include
from django.urls import path

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

urlpatterns = [
    #Dajaxice URLS
    path(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
]
