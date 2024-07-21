from rest_framework import serializers
from backend.models import ChatBot

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBot
        fields = ['id', 'text_input', 'gemini_output', 'date']
        read_only_fields = ['id', 'gemini_output']

    def validate_text_input(self, value):
        # Add custom validation logic here
        if not value.strip():
            raise serializers.ValidationError("Input text cannot be empty.")
        return value
