from django.contrib import admin

# Register your models here.
from .models import User, BloodRequest, Response

admin.site.register(User)
admin.site.register(BloodRequest)
admin.site.register(Response)