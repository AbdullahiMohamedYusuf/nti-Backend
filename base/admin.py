from django.contrib import admin
from .models import UseProfile, Company,Addresses,Pictures
# Register your models here.
admin.site.register(UseProfile)
admin.site.register(Company)
admin.site.register(Addresses)

class PictureAdmin(admin.ModelAdmin):
    readonly_field = ('id')

admin.site.register(Pictures, PictureAdmin)