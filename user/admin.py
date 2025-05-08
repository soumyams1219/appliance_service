from django.contrib import admin
from .models import Service
from .models import Schedule
# Register your models here.
admin.site.register(Service)
admin.site.register(Schedule)
