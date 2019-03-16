from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=100, allow_blank=False, required=True)
    # photo = serializers.URLField(allow_blank=True, required=False)
    # password = serializers.CharField(max_length=128, required=True, allow_blank=False, min_length=6)
    # bio = serializers.CharField(max_length=250, required=False, allow_blank=True)
    # email = serializers.EmailField(allow_blank=False, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'bio', 'email', 'photo']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'location', 'bio', 'email', 'photo', 'birth_date'
                  , 'first_name', 'last_name', 'is_moderator', 'is_staff']


class UserRegisterSerializer(RegisterSerializer):
    bio = serializers.CharField(required=False, max_length=265)
    is_staff = serializers.BooleanField(default=False)
    is_moderator = serializers.BooleanField(default=False)

    def custom_signup(self, request, user):
        user.bio = self.validated_data.get('bio', '')
        user.is_staff = self.validated_data.get('is_staff', '')
        user.is_moderator = self.validated_data.get('is_moderator', '')
        user.save(update_fields=['bio', 'is_staff', 'is_moderator'])
