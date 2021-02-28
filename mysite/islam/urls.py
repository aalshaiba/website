from rest_framework import routers
from django.urls import path, include
from .views import PrayerView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('prayers', PrayerView.as_view())
]
