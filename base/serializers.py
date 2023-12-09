from rest_framework import serializers
from .models import Pictures, UseProfile, Addresses, Company
# Register your Serializers here.


class Addresses(serializers.ModelSerializer):
    Bild = serializers.ImageField(required=False, allow_null=True)
    Nummer = serializers.CharField(required=False, allow_blank=True)  # Making Nummer field optional
    Stjärnor = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Addresses
        fields = '__all__'
