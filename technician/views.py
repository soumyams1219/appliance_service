from django.shortcuts import render,redirect
from user.models import Schedule,Service
from guest.models import Customer
from administrator.models import TechnicianQualification
# Create your views here.
def home(request):
    customer = Customer.objects.get(user_id = request.user)
    technician = TechnicianQualification.objects.get(customer=customer)
    schedules = Schedule.objects.filter(technician = technician)
    return render(request,'technician/view_scheduled_request.html',context={'schedules':schedules})

def finish_request(request,id):
    service_instance = Service.objects.get(id=id)
    service_instance.status = "completed"
    service_instance.save()
    return redirect('technician:home')
