from rest_framework import serializers
from backend.models import ChatBot

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBot
        fields = ['id', 'text_input', 'gemini_output', 'date']
        read_only_fields = ['id', 'gemini_output', 'date', 'user']

    def validate_text_input(self, value):
        # Add custom validation logic here
        if not value.strip():
            raise serializers.ValidationError("Input text cannot be empty.")
        return value

    def create(self, validated_data):
        # Get the user from the context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
