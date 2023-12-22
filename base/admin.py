from django.contrib import admin
from .models import UseProfile, Company,Pictures
# Register your models here.
admin.site.register(UseProfile)
admin.site.register(Company)

class PictureAdmin(admin.ModelAdmin):
    readonly_field = ('id')
class UseProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user_ID',)
    
admin.site.register(Pictures, PictureAdmin)