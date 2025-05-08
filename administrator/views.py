from django.shortcuts import render,redirect
from .models import Product
from django.contrib import messages
from .models import Issue
from .models import TechnicianQualification
from guest.models import Customer,Role
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from user.models import Service,Schedule
#this will be used for adding products by admin

def home(request):
    if request.method == 'POST':
        product = request.POST['product']
        if product=="":
            messages.error(request,"Product should not be empty")
        exist,create = Product.objects.get_or_create(product=product)
        if create:
            messages.success(request,"Product added successfully")
            return redirect('administrator:home')
        else:
            messages.warning(request,"Product already existing")
        product_instance = Product(product=product)
        product_instance.save()
    products = Product.objects.all()
    return render(request,'administrator/home.html',context={'products':products})
        

def add_issues(request):
    if request.method == 'POST':
        product_id = request.POST['product']
        product_obj = Product.objects.get(id=product_id)
        added = 0
        for key,value in request.POST.items():
            if key.startswith('issue_'):
                exist,create = Issue.objects.get_or_create(product=product_obj,issue=value.strip())
                added+=1
        messages.success(request,f"{added} Issue(s) added successfully")
        return redirect('administrator:add-issues')
        
    product = Product.objects.all()
    issues = Issue.objects.all()
    return render(request,'administrator/add_common_issues.html',context={'products':product,'issues':issues})
 
# viewing request for services
def view_requests(request):
    if request.method == 'POST':
        pass
    requests = Service.objects.filter(status='pending')
    return render(request,'administrator/view_requests.html',context={'requests':requests})

def edit_product(request):
    if request.method == 'POST':
        product = request.POST['product']
        if product=="":
            messages.error(request,"Product should not be empty")
        id = request.POST.get('id')
        product_obj = Product.objects.get(id=id)

        product_obj.product=product
        product_obj.save()
        messages.success(request,"Product updated successfully")
        return redirect('administrator:home')
    id = request.GET.get('id')
    product_obj = Product.objects.get(id=id)
    return render(request,'administrator/edit_product.html',context={'products':product_obj})

def delete_product(request,id):
    product_obj = Product.objects.get(id=id)
    product_obj.delete()
    messages.success(request,"Product deleted successfully")
    return redirect('administrator:home')

def edit_issue(request):
    if request.method == 'POST':
        issue_id = request.POST['issueid']
        product_id = request.POST['product']
        product_obj = Product.objects.get(id=product_id)
        issue_obj = Issue.objects.get(id=issue_id)
        
        issue_obj.product = product_obj
        issue_obj.issue = request.POST['issue']
        issue_obj.save()
        
        messages.success(request,"Issue updated successfully")
        return redirect('administrator:add-issues')
        
    id = request.GET.get('id')
    issue_obj = Issue.objects.get(id=id)
    print("issue:",issue_obj.issue)
    return render(request,'administrator/edit_issues.html',context={'issues':issue_obj,'issue_id':id})

def delete_issue(request,id):
    issue_obj = Issue.objects.get(id=id)
    issue_obj.delete()
    messages.success(request,"Issue deleted successfully")
    return redirect('administrator:add-issues')

def send_password(user,password):
    subject = "Email and Password - Technician ( Smart Appliance service )"

    if user:
        name = user.first_name
        to_email = user.email
    else:
        print("An error occured")
    print("email:",to_email,"password:",password,"name:",name)
    message = "Dear " + name + ", Your email for logging into the smart appliance services is " + to_email + " and password is " + password
    from_email = "soumyams999@gmail.com"
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [to_email])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")

import random
def generate_password(name):
    random_number = random.randint(10000,99999)
    password = name+'@'+str(random_number)
    return password

def add_technician(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        qualification = request.POST['qualification']
        years_of_exp = request.POST['years_of_exp']
        email = request.POST['email']
        pincode = request.POST['pincode']
        password = generate_password(name)
        user = User.objects.create_user(username=email,email=email,first_name=name,is_active=False,password=password)
        user.save()
        role = Role.objects.create(user_id = user,role='technician')
        role.save()
        customer = Customer(address=address,pincode=pincode,phone=phone,user_id=user)
        customer.save()
        technician_instance = TechnicianQualification(customer=customer,qualification=qualification,years_of_exp=years_of_exp)
        technician_instance.save()
        send_password(user,password)
        messages.success(request,"Technician details added successfully")
        return render(request,'administrator/add_technician.html')
    technician_obj = TechnicianQualification.objects.select_related('customer__user_id')
    return render(request,'administrator/add_technician.html',context={'technician_details':technician_obj})

def edit_technician(request):
    id = request.GET.get('id')
    technician_instance = TechnicianQualification.objects.get(id=id)
    customer_instance = technician_instance.customer
    user_instance = customer_instance.user_id
    if request.method == 'POST':
        user_instance.first_name = request.POST['name']
        user_instance.email = request.POST['email']
        user_instance.save()
        customer_instance.address = request.POST['address']
        customer_instance.pincode = request.POST['pincode']
        customer_instance.phone = request.POST['phone']
        customer_instance.save()
        technician_instance.qualification = request.POST['qualification']
        technician_instance.years_of_exp = request.POST['years_of_exp']
        technician_instance.save()
        messages.success(request,"Technician details updated successfully")
        return redirect('administrator:add-technician')
    return render(request,'administrator/edit_technician.html',context={'technician':technician_instance,'customer':customer_instance,'user':user_instance})

def delete_technician(request,id):
    technician_instance = TechnicianQualification.objects.get(id=id)
    customer_instance = technician_instance.customer
    user_instance = customer_instance.user_id
    customer_instance.delete()
    user_instance.delete()
    technician_instance.delete()
    messages.success(request,"Technician details deleted successfully")
    return redirect('administrator:add-technician')

def reject_request(request,id):
    service_instance = Service.objects.get(id=id)
    service_instance.status = "rejected"
    service_instance.save()
    requests = Service.objects.filter(status='pending')
    messages.success(request,"Service request rejected successfully")
    return render(request,'administrator/view_requests.html',context={'requests':requests})

def accept_request(request):
    id = request.GET.get('id')
    service_instance = Service.objects.get(id=id)
    service_instance.status = "accepted"
    service_instance.save()
    technician_obj = TechnicianQualification.objects.select_related('customer__user_id')
    return render(request,'administrator/schedule_requests.html',context={'requests':service_instance,'technicians':technician_obj})

def schedule_request(request):
    if request.method == 'POST':
        service_id = request.POST['service_request_id']
        #print("service_id",service_id)
        service_address = request.POST['service_address']
        technician = request.POST['technician']
        schedule_date = request.POST['schedule_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        technician_instance = TechnicianQualification.objects.get(id=technician)
        service_instance = Service.objects.get(id=service_id)
        schedule_instance = Schedule(service=service_instance,service_address=service_address,technician=technician_instance,schedule_date=schedule_date,start_time=start_time,end_time=end_time)
        schedule_instance.save()
        messages.get_messages(request).used=True
        messages.success(request,"Service scheduled successfully")
        requests = Service.objects.filter(status='pending')
        return render(request,'administrator/view_requests.html',context={'requests':requests})

def view_all_requests(request):
    all_requests = Service.objects.all()
    return render(request,'administrator/view_all_requests.html',context={'servicerequests':all_requests})
           

