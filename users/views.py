from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Supervisor, Reviewer
from .serializers import UserSerializer, RegisterSerializer, SupervisorSerializer, ReviewerSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        # Determine if user is Supervisor or Reviewer
        if Supervisor.objects.filter(user=user).exists():
            user_data["role"] = "supervisor"
            user_data["department"] = Supervisor.objects.get(user=user).department
        elif Reviewer.objects.filter(user=user).exists():
            user_data["role"] = "reviewer"
        else:
            user_data["role"] = "regular_user"

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid Credentials or Inactive Account"}, status=status.HTTP_400_BAD_REQUEST)
