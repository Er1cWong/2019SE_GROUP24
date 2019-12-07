from django.contrib import admin
# Register your models here.

from .models import DataSet, UserProfile
admin.site.register(DataSet)
admin.site.register(UserProfile)
