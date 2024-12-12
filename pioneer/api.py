from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from .views import generate_response


@api_view(['GET', 'POST'])
def chat_api(request):
    if request.method == 'GET':
        messages = ChatMessage.get_chat_history()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        prompt = request.data.get('prompt', '')
        if prompt:
            user_message = ChatMessage.objects.create(role="user", content=prompt)
            response = generate_response(prompt)
            assistant_message = ChatMessage.objects.create(role="assistant", content=response)
            return Response({'user': user_message.content, 'assistant': assistant_message.content})
        return Response({'error': 'Invalid input'}, status=400)
