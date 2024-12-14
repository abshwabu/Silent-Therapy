from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from backend.models import GroupChat, GroupMessage, PrivateChat, PrivateMessage
from .serializers import (
    GroupChatSerializer, GroupMessageSerializer,
    PrivateChatSerializer, PrivateMessageSerializer
)

class PrivateChatViewSet(viewsets.ModelViewSet):
    serializer_class = PrivateChatSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return PrivateChat.objects.filter(participants=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat = self.get_object()
        if request.user not in chat.participants.all():
            return Response(
                {"error": "You are not a participant in this chat"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PrivateMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupChatViewSet(viewsets.ModelViewSet):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return GroupChat.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        chat = serializer.save(host=self.request.user)
        chat.members.add(self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        chat = self.get_object()
        chat.members.add(request.user)
        return Response(self.get_serializer(chat).data)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        chat = self.get_object()
        if request.user == chat.host:
            return Response(
                {"error": "Host cannot leave the chat"},
                status=status.HTTP_400_BAD_REQUEST
            )
        chat.members.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat = self.get_object()
        if request.user not in chat.members.all():
            return Response(
                {"error": "You are not a member of this chat"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = GroupMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
