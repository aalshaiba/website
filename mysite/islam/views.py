from rest_framework.views import APIView, Response
from .prayers import get_prayer


class PrayerView(APIView):

    def get(self, request):
        return Response(get_prayer())
