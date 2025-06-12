# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from administrator.models import Product
# from administrator.models import Issue
# from .models import Service
# from django.contrib import messages
# from django.contrib.auth.models import User
# from guest.models import Customer
# from rest_framework import generics
# from .serializer import *
# from rest_framework.permissions import IsAuthenticated
# # Create your views here.
# @login_required(login_url = 'guest:login')
# def home(request):
#     if request.method == 'POST':
#         product = request.POST['product']
#         issue = request.POST['complaint']
#         product_instance = Product.objects.get(id=product)
#         if issue=='other':
#             issue = request.POST['manualComplaint']
#             issue_obj = Issue.objects.create(product=product_instance,issue=issue)
#         else:
#             issue_obj = Issue.objects.get(id=issue)
#         user_id = request.user.id
#         user = User.objects.get(id=user_id)
#         customer = Customer.objects.get(user_id = user)
        
       
#         service_instance = Service(customer=customer,product=product_instance,issue=issue_obj)
#         service_instance.save()
#         messages.get_messages(request).used= True
#         messages.success(request,"Service request added successfully")
#         products = Product.objects.all()
#         issues = Issue.objects.all()
#         return render(request,'user/home.html',context={'products':products,'issues':issues})
#     products = Product.objects.all()
#     issues = Issue.objects.all()
#     return render(request,'user/home.html',context={'products':products,'issues':issues})

# @login_required(login_url = 'guest:login')
# def view_requests(request):
#     return render(request,'user/view_requests.html')

# @login_required(login_url = 'guest:login')
# def track_status(request):
#    customer = Customer.objects.get(user_id=request.user)
#    services = Service.objects.filter(customer=customer)
#    return render(request,'user/track_status.html',context={'services':services})

# class servicerequestCreationAPIView(generics.CreateAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer

from rest_framework import generics, permissions
from .models import Service, Schedule
from .serializer import ServiceSerializer
from rest_framework.permissions import AllowAny  # Allow all users

# --------------------
# Service Views (No Auth)
# --------------------

class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Returns all services without filtering by user
        return Service.objects.all()

class ServiceCreateAPIView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Since user is anonymous, you need to handle customer manually or skip it
        serializer.save()

class ServiceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class ServiceUpdateAPIView(generics.UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class ServiceDeleteAPIView(generics.DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

# --------------------
# Schedule Views (No Auth)
# --------------------

# class ScheduleListAPIView(generics.ListAPIView):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     permission_classes = [AllowAny]

# class ScheduleCreateAPIView(generics.CreateAPIView):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     permission_classes = [AllowAny]

# class ScheduleRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     permission_classes = [AllowAny]

# class ScheduleUpdateAPIView(generics.UpdateAPIView):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     permission_classes = [AllowAny]

# class ScheduleDeleteAPIView(generics.DestroyAPIView):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
#     permission_classes = [AllowAny]




