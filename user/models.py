from django.db import models
from administrator.models import Product,Issue,TechnicianQualification
from guest.models import Customer
# Create your models here.
class Service(models.Model):
    status_choices = [('pending','Pending'),('completed','Completed'),('accepted','Accepted'),('rejected','Rejected'),('paid','Paid')]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    date_requested = models.DateField(auto_now_add=True)
    status = models.CharField(choices=status_choices,default='pending')

    def __str__(self):
        return self.customer.user_id.first_name+"-"+self.issue.issue

class Schedule(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    technician = models.ForeignKey(TechnicianQualification,on_delete =models.CASCADE)
    service_address = models.TextField()

    def __str__(self):
        return self.service.issue.issue+"-"+self.technician.customer.user_id.first_name
