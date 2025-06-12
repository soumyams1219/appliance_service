from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','first_name','password']
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['user','address','phone','pincode','otp']
        read_only_fields = ['otp']
    def create(self,validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        otp = self.context.get('otp')
        customer = Customer.objects.create(user_id=user,otp=otp,**validated_data)
        return customer

class RoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    class Meta:
        model = Role
        fields = '__all__'