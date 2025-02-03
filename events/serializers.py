from rest_framework import serializers
from .models import UserProfile, ContactInfo, EventGroup, Event

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password', 'first_name','last_name', 'image']

    def create(self, validated_data):
        # Create a new user with a hashed password
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            image=validated_data.get('image')
        )
        return user


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'phone', 'email']


class EventGroupSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EventGroup
        fields = ['id', 'name', 'description', 'created_by']

# class EventSerializer(serializers.ModelSerializer):
#     contacts = ContactInfoSerializer(many=True)

#     class Meta:
#         model = Event
#         fields = ['id', 'title', 'description', 'group', 'contacts', 'tagged_users', 'created_at', 'file']

#     def create(self, validated_data):
#         contacts_data = validated_data.pop('contacts', [])
#         tagged_users_data = validated_data.pop('tagged_users', [])
        
#         event = Event.objects.create(**validated_data)
        
#         # Add contacts to event
#         for contact_data in contacts_data:
#             contact, _ = ContactInfo.objects.get_or_create(**contact_data)
#             event.contacts.add(contact)
        
#         # Add tagged users to event
#         for user in tagged_users_data:
#             event.tagged_users.add(user)
        
#         return event

# In serializers.py (Backend)
class EventSerializer(serializers.ModelSerializer):
    contacts = ContactInfoSerializer(many=True)
    tagged_users = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'user', 'group', 'contacts', 'tagged_users', 'file']

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', [])
        tagged_users_data = validated_data.pop('tagged_users', [])

        # Create the event
        event = Event.objects.create(**validated_data)

        # Add contacts (ensure all fields are provided)
        for contact_data in contacts_data:
            contact, _ = ContactInfo.objects.get_or_create(**contact_data)
            event.contacts.add(contact)

        # Add tagged users (validate IDs exist)
        event.tagged_users.set(tagged_users_data)

        return event