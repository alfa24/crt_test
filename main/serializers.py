from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_registration.api.serializers import DefaultRegisterUserSerializer
from rest_framework import serializers

from main.models import UserProfile, City, Advert

User = get_user_model()


class CitySerializer(serializers.ModelSerializer):
    """Город."""
    class Meta:
        model = City
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    """Профиль пользователя."""
    city = CitySerializer()

    class Meta:
        model = UserProfile
        fields = ['city']


class UserSerializer(serializers.ModelSerializer):
    """Пользователь."""
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class SimpleUserSerializer(serializers.ModelSerializer):
    """Пользователь с основными полями."""
    class Meta:
        model = User
        fields = ['id', 'username']


class CreateUserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        model = UserProfile
        fields = ['city']


class RegisterUserSerializer(WritableNestedModelSerializer, DefaultRegisterUserSerializer):
    """Сериализатор для процесса регистрации пользователя."""
    profile = CreateUserProfileSerializer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = list(self.Meta.fields)
        self.Meta.fields = fields + ['profile']


class UserAdvertSerializer(serializers.ModelSerializer):
    """Сериализатор для объявлений конкретного пользователя."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context['request'].user

    def validate_user(self, value):
        if self.user != value:
            raise ValidationError({'user': 'You can only specify your user '})
        return value

    def validate(self, attrs):
        if not attrs.get('user'):
            attrs['user'] = self.user
        return super().validate(attrs)

    class Meta:
        model = Advert
        fields = ['id', 'name', 'user', 'city', 'body', 'price']


class AdvertDetailSerializer(serializers.ModelSerializer):
    """Сериализатор объявления с детальной информацией."""
    user = SimpleUserSerializer()
    city = CitySerializer()

    class Meta:
        model = Advert
        fields = ['id', 'name', 'user', 'city', 'body', 'price']
