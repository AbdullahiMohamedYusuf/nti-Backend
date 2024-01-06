from rest_framework import serializers
from .models import Pictures, UseProfile, Company,Pictures, profilePicture
from django.contrib.auth import get_user_model

# Register your Serializers here.
User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username):
            raise serializers.ValidationError("Username already exists")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        if not any(char.isupper() for char in password) or len(password) <= 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain at least one uppercase letter")

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UseProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UseProfile
        fields = ('user_ID',
                  'first_name', 'last_name', 'description', 'phone_number')

class UseCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class BannerUpload(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = '__all__'

class ProfileBanner(serializers.ModelSerializer):
    class Meta:
        model = profilePicture
        fields = '__all__'