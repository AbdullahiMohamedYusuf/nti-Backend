from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UseProfile(models.Model):
    user_ID = models.IntegerField(null=False, default=0)
    profile_picture = models.ImageField(upload_to="user/profile", null=True, blank=True)
    banner_picture = models.ImageField(upload_to="user/profile", blank=True, null=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=True)
    phone_number = models.IntegerField(null=True)


class Pictures(models.Model):
    user_ID_P = models.IntegerField(null=False, default=0)
    company_uploads = models.ImageField(upload_to="user/uploads")

    def __str__(self):
        return "Picture"

class profilePicture(models.Model):
    user_ID_B = models.IntegerField(null=False, default=0)
    profile_uploads = models.ImageField(upload_to="user/profile")

    def __str__(self):
        return "profile"



class Company(models.Model):
    user_ID_C = models.IntegerField(null=False, default=0)

    CompanyName = models.CharField(max_length=200, null=True, blank=False)
    CompanyNumber = models.IntegerField(null=True)
    companyEmail = models.CharField(max_length=400, blank=False, null=True)
    Address = models.CharField(
        max_length=300, blank=False, default="unknown", null=True)

    Stad = models.CharField(max_length=200, blank=False,
                            default='Stockholm', null=True)
    Postnummer = models.CharField(
        max_length=200, blank=False, default="1234", null=True)
    Typ = models.CharField(max_length=100, blank=False,
                           default="unknown", null=True)
    Bild = models.ImageField(upload_to="user/find", null=True, blank=True)
    
    

    def __str__(self):
        return "Company"

