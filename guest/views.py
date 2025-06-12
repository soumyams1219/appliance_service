# from django.shortcuts import render,redirect
# from .models import Customer,Role
# from django.contrib.auth.models import User
# from django.contrib import messages
# import random
# from rest_framework import generics
# from .serializer import *
# from django.core.mail import BadHeaderError, send_mail
# from django.http import HttpResponse, HttpResponseRedirect
# from rest_framework.pagination import PageNumberPagination
# from .pagination import MyPagination
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters

# def send_otp(cust_id, otp):
#     print(f"{cust_id},{otp}")
#     try:
#         user = User.objects.get(id=cust_id)
#         name = user.first_name
#         to_email = user.email

#         subject = "One Time Password - Registration (Smart Appliance Service)"
#         message = f"Dear {name},\n\nYour OTP (One Time Password) for logging into the Smart Appliance Services is: {otp}\n\nThank you!"
#         from_email = "soumyams999@gmail.com"

#         if subject and message and from_email:
#             try:
#                 send_mail(subject, message, from_email, [to_email])
#                 return HttpResponse("OTP sent successfully.")
#             except BadHeaderError:
#                 return HttpResponse("Invalid header found.")
#         else:
#             return HttpResponse("Missing email content.")
      

#     except User.DoesNotExist:
#         return HttpResponse("User not found.")
#     except Exception as e:
#         return HttpResponse(f"An error occurred while sending OTP: {str(e)}")

# def generate_otp():
#     # generates an otp number 
#     return str(random.randint(100000,999999))

# def index(request):
#     # index view shows the landing page
#     # by default the request will be GET
#     if request.method == 'GET':
#         return render(request,'index.html')
#     # Handling malicious requests
#     else:
#          return HttpResponse('<h1>Request is Invalid</h1>')

# def register(request):
#     if request.method == 'POST':
#         cust_name = request.POST.get('customerName')
#         phone = request.POST.get('phoneNumber')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         pincode = request.POST.get('pincode')
#         password = request.POST.get('password')
#         otp = generate_otp()
#         #print("custname:",cust_name)
#         #print("phone:",phone)
#         #print("email:",email)
#         #print("address:",address)
#         #print("pincode:",pincode)
#         #print("password:",password)
#         user = User.objects.create_user(username=email,email=email,first_name=cust_name,is_active=False,password=password)
#         customer = Customer(address=address,pincode=pincode,phone=phone,otp=otp,user_id=user)
#         user.save()
#         customer.save()
#         cust_id = user.id
#         role = Role(user_id=user,role='user')
#         role.save()
#         send_otp(cust_id,otp)
#         request.session['cust_id'] = cust_id
#         return render(request,'verify_otp.html',context = {'cust_id':cust_id,'email':email})

#     return render(request,'index.html')

# def verify_otp(request):
#     if request.method == 'POST':
#         cust_id = request.POST.get('cust_id')
#         otp = request.POST.get('otp')
#         customer = Customer.objects.get(user_id=cust_id)
#         if customer.otp == otp :
#             messages.success(request,"Your OTP verified successfully")
#             user = User.objects.get(id=cust_id)
#             user.is_active = True
#             user.save()
#             return render(request,'login.html')
#         cust_id = request.session['cust_id']
#         otp = generate_otp()
#         customer.otp = otp
#         send_otp(cust_id,otp)
#         messages.error(request,"OTP Verification failed, New OTP has been sent to your registered email")
#         return render(request,'verify_otp.html',context={'cust_id':cust_id})
    
# from django.contrib.auth import authenticate,login
# def login_view(request):
#     if request.method == 'POST':
#         email =  request.POST['email']
#         password = request.POST.get('password')
#         #print("email:",email)
#         #print("password:",password)
#         user = authenticate(request,username=email,password=password)
#         #print("user:",user)
#         #print("username:",user.first_name)
#         if user is not None:
#             login(request,user)
#             role_instance = Role.objects.get(user_id=user)
#             role = role_instance.role
#             #print("role:",role)
#             if role == 'admin':
#                 return redirect('/administrator')
#             if role == 'technician':
#                 return redirect('/technician')
#             return redirect('/user')
#         else:
#             messages.error(request,"Invalid username or password / User account not registered")
#             return redirect('guest:login')
#     return render(request,'login.html')

# from django.contrib.auth import logout
# def logout_view(request):
#     logout(request)
#     messages.success(request,"Successfully logged out from the account")
#     return render(request,'login.html')

# class RoleListCreationAPIView(generics.ListCreateAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     pagination_class = MyPagination
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['role']
#     search_fields = []
#     ordering_fields = ['user_id']
#     ordering = ['user_id']
#     def get_queryset(self):
#         queryset = Role.objects.all()
#         search = self.request.query_params.get('search')
#         if search and search.isdigit():
#             queryset = queryset.filter(user_id=int(search))
#         return queryset

# class RoleListAPIView(generics.ListAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

# class RoleRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
    
# class RoleUpdateAPIView(generics.UpdateAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

# class RoleDeleteAPIView(generics.DestroyAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

from rest_framework.response import Response
from rest_framework import generics,status
from .models import *
from .serializer import *
import random
from django.core.mail import send_mail,BadHeaderError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .custom_authentication import CsrfExemptSessionAuthentication

def generate_otp():
# generates an otp number
    return str(random.randint(100000,999999))

def send_otp(email,name,otp):
    subject = 'One time password - registration for appliance service'
    message = f"Dear {name},\n\nYour OTP (One Time Password) for logging into the Smart Appliance Services is: {otp}\n\nThank you!"
    from_email = 'soumyams999@gmail.com'
    send_mail(subject,message,from_email,[email])

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('user', {}).get('username')
        if User.objects.filter(username=email).exists():
            return Response({'message': "User email is already existing"}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        serializers = self.get_serializer(data=request.data, context={'otp': otp})
        serializers.is_valid(raise_exception=True)
        customer = serializers.save()
        Role.objects.create(user_id=customer.user_id, role='user')

        try:
            send_otp(customer.user_id.email, customer.user_id.first_name, otp)
        except BadHeaderError:
            return Response({'message': "Invalid header found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f"Error sending OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': "User registered successfully", 'customer_id': customer.user_id.id}, status=status.HTTP_201_CREATED)

class VerifyotpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        cust_id = request.data.get('cust_id')
        otp = request.data.get('otp')
        customer = get_object_or_404(Customer,user_id=cust_id)
        
        if customer.otp==otp:
            user = customer.user_id
            user.is_active = True
            user.save()
            return Response({'message':"OTP verified successfully"})
        else:
            new_otp = generate_otp()
            customer.otp = new_otp 
            customer.save()
            send_otp(customer.user_id.email,customer.user_id.first_name,new_otp)
            return Response({'message':"otp verification failed,new otp send to email"})

class LoginAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,username=email,password=password)
        if user is not None:
            if not user.is_active:
                return Response({'message':"user account not active"},status=status.HTTP_400_BAD_REQUEST)
            login(request,user)
            role_instance = Role.objects.filter(user_id=user).first()
            role = role_instance.role if role_instance else None
            return Response({'message':"Login successfull",'role':role})
        else:
            return Response({'message':"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        logout(request)
        return Response({'message':"logout successfully"},status=status.HTTP_200_OK)

        
            








    
