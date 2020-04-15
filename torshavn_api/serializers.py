from rest_framework import serializers
from torshavn_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our AIView"""
    name = serializers.CharField(max_length=10)

class UserSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}

class MarkerSerializer(serializers.ModelSerializer):
    """Serializes marker items"""
    class Meta:
        model = models.Marker
        fields = ('id', 'draggable', 'animation', 'image_path', 'label', 'description', 'icon_path', 'lat', 'lng')
