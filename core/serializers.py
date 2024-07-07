from rest_framework import serializers
from .models import User, Organization

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_userId(self, value):
        if User.objects.filter(userId=value).exists():
            raise serializers.ValidationError("User ID must be unique.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email must be unique.")
        return value

    def validate_firstName(self, value):
        if not value:
            raise serializers.ValidationError("First name must not be null.")
        return value

    def validate_lastName(self, value):
        if not value:
            raise serializers.ValidationError("Last name must not be null.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password must not be null.")
        return value

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['orgId', 'name', 'description']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name must not be null.")
        return value
