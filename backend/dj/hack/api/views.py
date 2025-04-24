from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .geminiKey import Key
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=Key)

# Create a Gemini model (for text generation)
model = genai.GenerativeModel("gemini-2.0-flash")  # Use "gemini-pro-vision" for image+text

# Start a chat session (holds context)
chat = model.start_chat(history=[])

class GenerateAIContentView(APIView):
    def post(self, request):
        try:
            # Get user prompt from the request body
            prompt = "hi"
            if not prompt:
                return Response({"error": "Missing prompt"}, status=status.HTTP_400_BAD_REQUEST)

            # Send message to Gemini model
            response = chat.send_message(prompt)

            return Response({"generated_text": response.text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
