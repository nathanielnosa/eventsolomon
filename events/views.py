from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny


from .models import UserProfile, ContactInfo, EventGroup, Event, Media
from .serializers import (
    UserProfileSerializer, ContactInfoSerializer, 
    EventGroupSerializer, EventSerializer, MediaSerializer
)


class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

class EventView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id=None):
        if event_id:
            event = Event.objects.filter(id=event_id).first()
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = EventSerializer(event)
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Set logged-in user as the creator
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventGroupView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = EventGroup.objects.all()
        serializer = EventGroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
