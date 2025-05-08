from django.contrib import admin
from .models import Product
from .models import Issue
from .models import TechnicianQualification
# Register your models here.
admin.site.register(Product)
admin.site.register(Issue)
admin.site.register(TechnicianQualification)