from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from administrator.models import Product
from administrator.models import Issue
from .models import Service
from django.contrib import messages
from django.contrib.auth.models import User
from guest.models import Customer
# Create your views here.
@login_required(login_url = 'guest:login')
def home(request):
    if request.method == 'POST':
        product = request.POST['product']
        issue = request.POST['complaint']
        product_instance = Product.objects.get(id=product)
        if issue=='other':
            issue = request.POST['manualComplaint']
            issue_obj = Issue.objects.create(product=product_instance,issue=issue)
        else:
            issue_obj = Issue.objects.get(id=issue)
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(user_id = user)
        
       
        service_instance = Service(customer=customer,product=product_instance,issue=issue_obj)
        service_instance.save()
        messages.get_messages(request).used= True
        messages.success(request,"Service request added successfully")
        products = Product.objects.all()
        issues = Issue.objects.all()
        return render(request,'user/home.html',context={'products':products,'issues':issues})
    products = Product.objects.all()
    issues = Issue.objects.all()
    return render(request,'user/home.html',context={'products':products,'issues':issues})

@login_required(login_url = 'guest:login')
def view_requests(request):
    return render(request,'user/view_requests.html')

@login_required(login_url = 'guest:login')
def track_status(request):
   customer = Customer.objects.get(user_id=request.user)
   services = Service.objects.filter(customer=customer)
   return render(request,'user/track_status.html',context={'services':services})
