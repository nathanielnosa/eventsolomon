from rest_framework import serializers
from .models import UserProfile, ContactInfo, EventGroup, Event, Media


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password', 'fullname', 'image', 'address']

    def create(self, validated_data):
        # Create a new user with a hashed password
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
            address=validated_data['address'],
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


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file']


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    contacts = ContactInfoSerializer(many=True)
    tagged_users = serializers.StringRelatedField(many=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'created_by', 'group',
            'contacts', 'tagged_users', 'created_at', 'media'
        ]

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        tagged_users_data = validated_data.pop('tagged_users', [])
        event = Event.objects.create(**validated_data)

        for contact in contacts_data:
            contact_obj, _ = ContactInfo.objects.get_or_create(**contact)
            event.contacts.add(contact_obj)

        for tagged_user in tagged_users_data:
            user = UserProfile.objects.get(username=tagged_user)
            event.tagged_users.add(user)

        return event