from rest_framework import serializers
from backend.models import GroupChat, GroupMessage, PrivateChat, PrivateMessage
from user.serializers import UserSerializer

class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

class PrivateChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = PrivateMessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChat
        fields = ['id', 'participants', 'messages', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return PrivateMessageSerializer(last_message).data
        return None

class GroupMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = GroupMessage
        fields = ['id', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

class GroupChatSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    messages = GroupMessageSerializer(many=True, read_only=True)

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'host', 'members', 'messages', 'created_at']
        read_only_fields = ['id', 'host', 'created_at']