from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
# Create your models here.
class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    # customer_email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    DHAKA_CITY = 'BD-C*'
    OUTSIDE_DHAKA_CITY = 'BD-O*'
    DIVISION_CHOICES = [
        (DHAKA_CITY, "Dhaka City"),
        (OUTSIDE_DHAKA_CITY, "Outside Dhaka City"),
    ]
    area = models.CharField(max_length=9, choices=DIVISION_CHOICES,blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "this is a default message.", blank=True, null=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    delivery_fees = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    grand_total = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.customer)
    
    def get_status(self):
        return self.status
    class Meta:
        ordering = ['-date']

    # def save(self, *args, **kwargs):
        # if not self.id:             
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)

class LineItem(models.Model):
    customer = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    # service = models.TextField()
    product = models.TextField()
    # description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)
   