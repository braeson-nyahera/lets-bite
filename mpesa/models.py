from django.db import models

# Create your models here.
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, blank=True, null=True) 
    phone_number = models.CharField(max_length=15)
    amount = models.IntegerField()
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True) 
    status = models.CharField(max_length=50, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)  
    transaction_date = models.DateTimeField(blank=True, null=True)  
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"Transaction {self.mpesa_receipt_number or self.transaction_id} - {self.status}"