from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from backend.models import ChatBot
from .serializers import ChatBotSerializer
import google.generativeai as genai
import logging

from api_key import api_key

# Configure Google Generative AI with your API key
genai.configure(api_key=api_key)

# Initialize the GenerativeModel outside the view to reuse it
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a therapist interacting with patients. Be careful and responsible. Make your answers as short as possible and give advice when you can.",
)

class ChatBotViewSet(viewsets.ModelViewSet):
    queryset = ChatBot.objects.all()
    serializer_class = ChatBotSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return ChatBot.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def ask_question(self, request):
        text = request.data.get("text_input")
        print(text)
        if not text:
            return Response({"error": "No text input provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat = model.start_chat()
            response = chat.send_message(text)
            logging.debug(f"Received response: {response}")

            if response and response.text:
                user = self.request.user
                ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
                response_data = {
                    "text": response.text,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Empty response from the model"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logging.error(f"Error while generating response: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
