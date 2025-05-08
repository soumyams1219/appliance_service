from django.shortcuts import render,redirect
from .models import Customer,Role
from django.contrib.auth.models import User
from django.contrib import messages
import random
# Create your views here.
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

def send_otp(cust_id, otp):
    print(f"{cust_id},{otp}")
    try:
        user = User.objects.get(id=cust_id)
        name = user.first_name
        to_email = user.email

        subject = "One Time Password - Registration (Smart Appliance Service)"
        message = f"Dear {name},\n\nYour OTP (One Time Password) for logging into the Smart Appliance Services is: {otp}\n\nThank you!"
        from_email = "soumyams999@gmail.com"

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [to_email])
                return HttpResponse("OTP sent successfully.")
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
        else:
            return HttpResponse("Missing email content.")
      

    except User.DoesNotExist:
        return HttpResponse("User not found.")
    except Exception as e:
        return HttpResponse(f"An error occurred while sending OTP: {str(e)}")

def generate_otp():
    # generates an otp number 
    return str(random.randint(100000,999999))

def index(request):
    # index view shows the landing page
    # by default the request will be GET
    if request.method == 'GET':
        return render(request,'index.html')
    # Handling malicious requests
    else:
         return HttpResponse('<h1>Request is Invalid</h1>')

def register(request):
    if request.method == 'POST':
        cust_name = request.POST.get('customerName')
        phone = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        password = request.POST.get('password')
        otp = generate_otp()
        #print("custname:",cust_name)
        #print("phone:",phone)
        #print("email:",email)
        #print("address:",address)
        #print("pincode:",pincode)
        #print("password:",password)
        user = User.objects.create_user(username=email,email=email,first_name=cust_name,is_active=False,password=password)
        customer = Customer(address=address,pincode=pincode,phone=phone,otp=otp,user_id=user)
        user.save()
        customer.save()
        cust_id = user.id
        role = Role(user_id=user,role='user')
        role.save()
        send_otp(cust_id,otp)
        request.session['cust_id'] = cust_id
        return render(request,'verify_otp.html',context = {'cust_id':cust_id,'email':email})

    return render(request,'index.html')

def verify_otp(request):
    if request.method == 'POST':
        cust_id = request.POST.get('cust_id')
        otp = request.POST.get('otp')
        customer = Customer.objects.get(user_id=cust_id)
        if customer.otp == otp :
            messages.success(request,"Your OTP verified successfully")
            user = User.objects.get(id=cust_id)
            user.is_active = True
            user.save()
            return render(request,'login.html')
        cust_id = request.session['cust_id']
        otp = generate_otp()
        customer.otp = otp
        send_otp(cust_id,otp)
        messages.error(request,"OTP Verification failed, New OTP has been sent to your registered email")
        return render(request,'verify_otp.html',context={'cust_id':cust_id})
    
from django.contrib.auth import authenticate,login
def login_view(request):
    if request.method == 'POST':
        email =  request.POST['email']
        password = request.POST.get('password')
        #print("email:",email)
        #print("password:",password)
        user = authenticate(request,username=email,password=password)
        #print("user:",user)
        #print("username:",user.first_name)
        if user is not None:
            login(request,user)
            role_instance = Role.objects.get(user_id=user)
            role = role_instance.role
            #print("role:",role)
            if role == 'admin':
                return redirect('/administrator')
            if role == 'technician':
                return redirect('/technician')
            return redirect('/user')
        else:
            messages.error(request,"Invalid username or password / User account not registered")
            return redirect('guest:login')
    return render(request,'login.html')

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    messages.success(request,"Successfully logged out from the account")
    return render(request,'login.html')