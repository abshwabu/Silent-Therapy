from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from rest_framework.authentication import TokenAuthentication


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()  # Show all rooms
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Optimize query by using select_related and prefetch_related"""
        return Room.objects.all()\
            .select_related('host')\
            .prefetch_related('current_users', 'messages')

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save(host=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        room = Room.objects.select_related('host').filter(pk=pk).first()
        if not room:
            return Response({"error": "Room with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room = self.get_object()
        room.current_users.add(request.user)
        room.save()
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_message(self, request, pk=None):
        room = self.get_object()
        if room.current_users.filter(pk=request.user.pk).exists():
            serializer = MessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(room=room, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "You are not allowed to send messages in this room"}, 
            status=status.HTTP_403_FORBIDDEN
        )
