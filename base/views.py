from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .models import UseProfile, Company
from .serializers import UseProfileSerializer, UserSignupSerializer, UseCompanySerializer
import json
from pathlib import Path
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        # Assuming 'user' is a User instance
        try:
            use_profile = user.profile.first()  # Retrieve the related UseProfile instance
            profile_picture_url = use_profile.profile_picture.url  # Get the profile picture URL
            # Set the URL in the token
            token['profile-picture'] = profile_picture_url
        except (UseProfile.DoesNotExist, AttributeError):
            # If no UseProfile exists for the user or no profile picture is found
            token['profile-picture'] = None

        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_staff:  # Assuming non-admin users are not staff
                login(request, user)  # Create a session for non-admin users
                return HttpResponse('Non-admin user logged in successfully.')
            else:
                return HttpResponse('Admin users are not allowed.')
        else:
            return HttpResponse('Invalid credentials.')


class UserProfileView(APIView):
    queryset = UseProfile.objects.all()
    # Renamed serializer to serializer_class
    serializer_class = UseProfileSerializer

    def get(self, request, *args, **kwargs):
        queryset = UseProfile.objects.all()

        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        # Assuming 'user_ID_C' is used in the frontend
        user_id = request.data.get('user_ID')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            # Log the error for debugging purposes
            print(f"User with ID {user_id} does not exist: {e}")
            return Response({'error': 'User does not exist or invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'user_ID': user_id,
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'description': request.data.get('description'),
            'phone_number': request.data.get('phone_number'),
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyView(APIView):
    queryset = Company.objects.all()
    serializer_class = UseCompanySerializer
    
    def get(self, request, *args, **kwargs):
        queryset = Company.objects.all()

        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_ID_C')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            print(f"User with ID {user_id} does not exist: {e}")
            return Response({'error': 'User does not exist or invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'user_ID_C': user_id,
            'CompanyName': request.data.get('companyName'),
            'CompanyNumber': request.data.get('number'),  # Match the key 'number' here
            'companyEmail': request.data.get('companyEmail'),
            'Address': request.data.get('Address'),
            'Stad': request.data.get('City'),  # Match the key 'City' here
            'Postnummer': request.data.get('postnummer'),  # Match the key 'postnummer' here
            'Typ': request.data.get('type'),  # Match the key 'type' here
        }

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')  # Retrieve email from request data

        if not email:
            return Response({"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)

        filter_email = User.objects.filter(email=email)
        if filter_email.exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
