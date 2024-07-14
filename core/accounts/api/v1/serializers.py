from typing import Any, Dict
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")
    image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "image",
            "description",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        valid_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "user is not verified"})
        valid_data["email"] = self.user.email
        valid_data["user_id"] = self.user.id
        return valid_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "user is not verified"})
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError("passwords does not match")
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)
