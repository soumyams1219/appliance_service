from rest_framework import serializers
from .models import *
from guest.models import *
from django.contrib.auth.models import User
from user.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

class TechnicianQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianQualification
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','email']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'