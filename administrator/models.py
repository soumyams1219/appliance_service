from django.db import models
from guest.models import Customer,Role

# Create your models here.
class Product(models.Model):
    product = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.product

class Issue(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    issue = models.CharField(max_length=255)

    def __str__(self):
        return self.product.product+'-'+self.issue

class TechnicianQualification(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    qualification = models.CharField()
    years_of_exp = models.CharField()


    def __str__(self):
        return self.customer.user_id.first_name
    

