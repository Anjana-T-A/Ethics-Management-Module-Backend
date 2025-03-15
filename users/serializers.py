from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Supervisor, Reviewer

DEPARTMENT_CHOICES = [
    "Faculty of Arts, Humanities and Social Sciences",
    "Faculty of Education and Health Sciences",
    "Kemmy Business School",
    "Faculty of Science and Engineering",
    "Irish World Academy of Music and Dance",
]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email","password"]

class SupervisorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Supervisor
        fields = "__all__"

class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["supervisor", "reviewer"], write_only=True)
    department = serializers.ChoiceField(choices=DEPARTMENT_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','role','department']

    def create(self, validated_data):
        role = validated_data.pop('role')
        department = validated_data.pop('department')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Assign role
        if role == 'supervisor':
            Supervisor.objects.create(user=user, department= department)  # Add department logic as needed
        elif role == 'reviewer':
            Reviewer.objects.create(user=user, department=department)

        return user

        