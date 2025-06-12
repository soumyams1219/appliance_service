from rest_framework import serializers
from .models import *
from administrator.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','product']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id','issue']
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Customer
        fields = ['id','user','user_id','address','pincode','phone']

class ServiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(),source='customer',write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),source='product',write_only=True)
    issue_id = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all(),source='issue',write_only=True)

    class Meta:
        model = Service
        fields = ['id','customer','product','issue','date_requested','status','customer_id','product_id','issue_id']