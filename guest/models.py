from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [ ('admin','Admin'),('user','User'),('technician','Technician') ]
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=255,choices=ROLE_CHOICES,default='user')
    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
    def _str_(self):
        return f"{self.user_id.first_name} - {self.role}"
    
class Customer(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    otp = models.CharField(max_length=6)
    class Meta:
        verbose_name = 'customer_address'
        verbose_name_plural = 'customer_addresss'

