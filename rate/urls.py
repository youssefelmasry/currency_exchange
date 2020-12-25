from django.urls import path
from rate.views import RateView

urlpatterns = [
    path("rate/", RateView.as_view())
]
