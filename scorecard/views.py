from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


class Teams(APIView):
    """
    List all teams
    """
    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class Venues(APIView):
    """
    List all venues
    """
    def get(self, request, format=None):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)