from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import Addresses
import json
from pathlib import Path



# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def home(request):
    file_path = Path(__file__).resolve().parent / 'capitalized_api_data (3).json'
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)

    addresses_to_create = []
    for entry in data_list:
        address = Addresses(
            address=entry.get('address', 'unknown'),
            namn=entry.get('namn', 'unknown'),
            city=entry.get('city', 'Stockholm'),
            postnummer=entry.get('postnummer', '1234'),
            typ=entry.get('typ', 'unknown'),
            bild=entry.get('bild', None),
            nummer=entry.get('nummer', 0),
            Stjärnor=entry.get('Stjärnor', 0)
        )
        addresses_to_create.append(address)

    try:
        Addresses.objects.bulk_create(addresses_to_create)
        return HttpResponse("Worked")
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return HttpResponse("Error occurred during bulk creation")
    


@api_view(['POST'])
def AddressView(request):
    data = request.data
    serializer = Addresses(data=data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response("Data processed successfully", status=201)
    else:
        return Response(serializer.errors, status=400)

