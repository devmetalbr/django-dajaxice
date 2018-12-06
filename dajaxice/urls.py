from django.urls import path

from .views import DajaxiceRequest


urlpatterns = [
    path(r'(.+)/', DajaxiceRequest.as_view(), name='dajaxice-call-endpoint'),
    path(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
]
