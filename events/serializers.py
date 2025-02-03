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
#     group = serializers.PrimaryKeyRelatedField(queryset=EventGroup.objects.all())
#     created_by = serializers.StringRelatedField(read_only=True)
#     contacts = ContactInfoSerializer(many=True)
#     tagged_users = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), many=True)

#     class Meta:
#         model = Event
#         fields = [
#             'id', 'title', 'description', 'created_by', 'group',
#             'contacts', 'tagged_users', 'created_at', 'file'
#         ]

#     def create(self, validated_data):
#         contacts_data = validated_data.pop('contacts')
#         tagged_users_data = validated_data.pop('tagged_users', [])
#         event = Event.objects.create(**validated_data)

#         # Add contacts to event
#         for contact in contacts_data:
#             contact_obj, _ = ContactInfo.objects.get_or_create(**contact)
#             event.contacts.add(contact_obj)

#         # Add tagged users to event (Handle as UserProfile instances)
#         for tagged_user in tagged_users_data:
#             event.tagged_users.add(tagged_user)  # Use UserProfile instance directly

#         return event

# class EventSerializer(serializers.ModelSerializer):

    # contact_name = serializers.CharField(write_only=True)
    # contact_email = serializers.EmailField(write_only=True)
    # contact_phone = serializers.CharField(write_only=True)
    # contact_address = serializers.CharField(write_only=True)

    # class Meta:
    #     model = Event
    #     fields = '__all__'
    #     extra_fields = ['contact_name', 'contact_email', 'contact_phone', 'contact_address']

    # def create(self, validated_data):
    #     # Extract contact info
    #     contact_info = {
    #         'name': validated_data.pop('contact_name'),
    #         'email': validated_data.pop('contact_email'),
    #         'phone': validated_data.pop('contact_phone'),
    #         'address': validated_data.pop('contact_address'),
    #     }
        
    #     # Create event
    #     event = super().create(validated_data)
    #     event.contact_info = contact_info
    #     event.save()
    #     return event

class EventSerializer(serializers.ModelSerializer):
    contacts = ContactInfoSerializer(many=True)  # Using serializer for contacts

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'group', 'contacts', 'tagged_users', 'created_at', 'file']
