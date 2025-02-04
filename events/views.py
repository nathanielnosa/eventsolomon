from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

import json

from .models import UserProfile, ContactInfo, EventGroup, Event
from .serializers import *

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
            # Generate JWT Token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "image": user.image.url if user.image else None,
                },
                "token": access_token,  # ✅ Return token
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access this endpoint
    def get(self, request):
        users = UserProfile.objects.all()  # Get all users from the database
        serializer = UserSerializer(users, many=True)  # Serialize all users
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventView(APIView):
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
        data = request.data.copy()

        # ===== 1. Process Group =====
        group_id = data.get("group")
        if not group_id:
            return Response({"error": "Group is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = EventGroup.objects.get(id=int(group_id))
        except (ValueError, EventGroup.DoesNotExist):
            return Response({"error": "Invalid group ID"}, status=status.HTTP_400_BAD_REQUEST)

        # ===== 2. Process Tagged Users =====
        tagged_users = request.data.getlist("tagged_users", [])  # 🚨 Use getlist() for multi-values
        try:
            tagged_users = [int(uid) for uid in tagged_users]
        except ValueError:
            return Response({"error": "Tagged users must be integer IDs"}, status=status.HTTP_400_BAD_REQUEST)

        # ===== 3. Process Contacts =====
        contacts_str = data.get("contacts", "[]")
        try:
            contacts = json.loads(contacts_str)  # Parse JSON string to list
        except json.JSONDecodeError:
            return Response({"error": "Invalid contacts format"}, status=status.HTTP_400_BAD_REQUEST)

        contact_ids = []
        for contact in contacts:
            if isinstance(contact, dict):
                # Validate required fields
                required = ["name", "email", "phone", "address"]
                if not all(k in contact for k in required):
                    return Response({"error": f"Missing contact fields. Required: {required}"}, status=400)
                # Create new contact
                new_contact = ContactInfo.objects.create(**contact)
                contact_ids.append(new_contact.id)
            else:
                return Response({"error": "Contacts must be objects"}, status=400)

        # ===== 4. Prepare final data =====
        data = {
            "title": data.get("title"),
            "description": data.get("description"),
            "user": request.user.id,
            "group": group.id,
            "contacts": contact_ids,
            "tagged_users": tagged_users,
            "file": data.get("file"),
        }
        print("b_s_Contacts:", contacts)
        print("b_s_Tagged Users:", tagged_users)
        print("b_s_Group ID:", group_id)
        # ===== 5. Validate & Save =====
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            print("Contacts:", contacts)
            print("Tagged Users:", tagged_users)
            print("Group ID:", group_id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # def post(self, request):
    #     data = request.data.copy()

    #     # Handle contacts: create new or use existing contact IDs
    #     contacts_data = data.get("contacts", [])
    #     contact_ids = []

    #     for contact in contacts_data:
    #         if isinstance(contact, dict):  # If a dict, create new contact
    #             new_contact = ContactInfo.objects.create(**contact)
    #             contact_ids.append(new_contact.id)
    #         else:
    #             contact_ids.append(contact)  # If an ID, add it directly

    #     data["contacts"] = contact_ids

    #     # Ensure group ID exists
    #     group_id = data.get("group")
    #     if not EventGroup.objects.filter(id=group_id).exists():
    #         return Response({"error": "Invalid group ID"}, status=status.HTTP_400_BAD_REQUEST)

    #     serializer = EventSerializer(data=data, context={"request": request})
    #     if serializer.is_valid():
    #         event = serializer.save(user=request.user)
    #         event.contacts.set(contact_ids)  # Set many-to-many relationship
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = EventGroup.objects.filter(created_by=request.user) 
        serializer = EventGroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# backend/events/views.py
class UserLookupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.GET.get('username')
        user = UserProfile.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=404)
        return Response({"id": user.id})