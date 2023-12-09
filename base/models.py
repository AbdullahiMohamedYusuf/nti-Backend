from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Pictures(models.Model):
    company_uploads = models.ImageField(upload_to="user/uploads")


class UseProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="user/profile")
    Banner_picture = models.ImageField(upload_to="user/profile")
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    UserCompany = models.CharField(max_length=100, null=True)
    Role = models.CharField(max_length=100, null=True)
    Description = models.CharField(max_length=300, null=True)
    PhoneNumber = models.IntegerField(null=True)

    def __str__(self):
        return self.first_name


class Company(models.Model):
    CompanyName = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=300, blank=False)
    CompanyNumber = models.IntegerField(null=True)
    CompanyOpening = models.TimeField(default=timezone.now)
    CompanyClosing = models.TimeField(default=timezone.now)
    company_uploads = models.ForeignKey(
        Pictures,
        related_name='companies_uploaded',
        on_delete=models.CASCADE,
        default=1  # Replace '1' with the default ID of an existing picture.
    )

    def __str__(self):
        return self.CompanyName


class Addresses(models.Model):
    Address = models.CharField(
        max_length=300, blank=False, default="unknown", null=False)
    Namn = models.CharField(max_length=200, blank=False,
                            default="unknown", null=False)
    Stad = models.CharField(max_length=200, blank=False,
                            default='Stockholm', null=False)
    Postnummer = models.CharField(
        max_length=200, blank=False, default="1234", null=False)
    Typ = models.CharField(max_length=100, blank=False,
                           default="unknown", null=False)
    Bild = models.ImageField(upload_to="user/find", null=True, blank=True)
    Nummer = models.CharField(max_length=300, default='', null=True, blank=True)
    Stjärnor = models.CharField(max_length=300, default='', null=True, blank=True)

    def __str__(self):
        return self.Address

    objects = models.Manager()

    class Meta:
        default_manager_name = 'objects'