# serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password_confirm', 'user_type', 
                 'restaurant_name', 'restaurant_address', 'restaurant_phone']
        extra_kwargs = {
            'password': {'write_only': True},
            'restaurant_name': {'required': False},
            'restaurant_address': {'required': False},
            'restaurant_phone': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        
        if not attrs.get('email') and not attrs.get('username'):
            raise serializers.ValidationError("Either email or username is required.")
        
        # If user is restaurant owner, require restaurant details
        if attrs.get('user_type') == 'restaurant_owner':
            if not attrs.get('restaurant_name'):
                raise serializers.ValidationError("Restaurant name is required for restaurant owners.")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        if not data.get('email') and not data.get('username'):
            raise serializers.ValidationError("Provide either email or username.")
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'user_type', 'restaurant_name', 
                 'restaurant_address', 'restaurant_phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'restaurant_name', 'restaurant_address', 'restaurant_phone']

    def validate(self, attrs):
        user = self.instance
        if user.is_restaurant_owner() and 'restaurant_name' in attrs and not attrs['restaurant_name']:
            raise serializers.ValidationError("Restaurant name cannot be empty for restaurant owners.")
        return attrs