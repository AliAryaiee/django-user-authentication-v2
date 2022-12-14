from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        User Register Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        # fields = "__all__"
        fields = ("first_name", "last_name", "email", "password")
        exclude = []
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data: dict):
        """
            Overriding Create Method
        """
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
        User Profile Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        # fields = "__all__"
        exclude = ["password"]
