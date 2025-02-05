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

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        contacts = validated_data.pop('contacts', [])
        tagged_users = validated_data.pop('tagged_users', [])

        event = Event.objects.create(**validated_data)

        # Use set() for ManyToMany fields
        event.contacts.set(contacts)
        event.tagged_users.set(tagged_users)

        return event