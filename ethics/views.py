# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EthicsForm
from .serializers import EthicsFormSerializer

@api_view(['POST'])
def submit_ethics_form(request):
    if request.method == 'POST':
        serializer = EthicsFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_reviewer_notification(request, ethics_form_id):
    result = notify_reviewer.apply_async(args=[ethics_form_id])
    return JsonResponse(result.get())