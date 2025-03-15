# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EthicsForm
from .serializers import EthicsFormSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import EthicsForm
from .serializers import EthicsFormSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_ethics_form(request):
    if request.method == 'POST':
        # Ensure the user is authenticated and is a supervisor
        if not hasattr(request.user, 'supervisor'):
            return Response({"detail": "User is not a supervisor."}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the supervisor associated with the authenticated user
        supervisor = request.user.supervisor

        # Add supervisor to the request data before validation
        data = request.data.copy()  # Make a mutable copy of the data
        data['supervisor'] = supervisor.id  # Assign supervisor's ID to the form data

        serializer = EthicsFormSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_reviewer_notification(request, ethics_form_id):
    result = notify_reviewer.apply_async(args=[ethics_form_id])
    return JsonResponse(result.get())   