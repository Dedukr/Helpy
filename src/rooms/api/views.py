from re import L
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rooms.models import Room
from .serializers import RoomSerializer
from rooms.api import serializers


@api_view(["GET"])
def get_routes(request):
    routes = ["GET api", "GET api/rooms", "GET api/rooms/:id"]
    return Response(routes)


@api_view(["GET"])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_detailed_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
