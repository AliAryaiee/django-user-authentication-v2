import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, permissions, status
from django.contrib.auth import get_user_model

from . import serializers
from App.settings import SECRET_KEY

User = get_user_model()


class UserRegister(APIView):
    """
        User Register Endpoint
    """

    def post(self, request):
        """
            Register User POST Request
        """
        serialized_user = serializers.UserRegisterSerializer(data=request.data)

        if serialized_user.is_valid(raise_exception=True):
            validated_data = serialized_user.validated_data
            user_db = serialized_user.create(validated_data)
            serialized_response = serializers.UserProfileSerializer(user_db)
            return Response(serialized_response.data)


class UserProfile(APIView):
    """
        User Profile Endpoint
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_user_object(self, user_id: int):
        """
            Find User by Username
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request):
        """
            Retrieve User Profile GET Request
        """
        JWT = request.headers["Authorization"].split(" ")[-1]
        if not JWT:
            raise exceptions.AuthenticationFailed("You Must Be Authenticated!")
        try:
            payload = jwt.decode(
                JWT,
                SECRET_KEY,
                algorithms=["HS256"]
            )
            db_user = self.get_user_object(user_id=int(payload["user_id"]))
            if db_user:
                serialized_data = serializers.UserProfileSerializer(
                    instance=db_user
                )
                return Response(serialized_data.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                "The Token Has Benn Expired!"
            )
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        return Response(
            {"response": "You Must Be Authenticated!"},
            status=status.HTTP_401_UNAUTHORIZED
        )
