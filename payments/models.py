from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Payment(models.Model):
    message = models.CharField(name='message',verbose_name='Message',max_length=600)
    name = models.CharField(name='name',verbose_name='Name',max_length=300,default='default',null=True,blank=True)
    sender = models.CharField(name='sender',verbose_name='Sender',max_length=250)
    number = models.CharField(name='number',verbose_name='Phone Number',max_length=13,default='default',null=True)
    transactionId = models.CharField(name='transactionId',verbose_name='Transaction Id',max_length=200,unique=True)
    amount = models.IntegerField(name='amount',verbose_name='Amount')
    is_valid = models.BooleanField(name='is_valid',default=False)
    valid_until = models.DateTimeField(name='due_date',null=True,blank=True)
    created = models.DateTimeField(name='created',auto_now_add=True)
    user = models.ForeignKey(to=CustomUser,null=True,blank=True,on_delete=models.CASCADE)

    def toJson(self):
        return {
            'message': self.message,
            'name': self.name,
            'sender': self.sender,
            'number': self.number,
            'transactionId': self.transactionId,
            'amount': self.amount,
            'created': self.created,
            'valid_until': self.valid_until,
            'user': self.user
        }

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payments'


class InvalidPayments(models.Model):
    message = models.CharField(name='message',verbose_name='Message',max_length=600)
    name = models.CharField(name='name',verbose_name='Name',max_length=300,null=True,blank=True)
    sender = models.CharField(name='sender',verbose_name='Sender',max_length=250,null=True,blank=True)
    number = models.CharField(name='number',verbose_name='Phone Number',max_length=13,null=True,blank=True)
    transactionId = models.CharField(name='transactionId',verbose_name='Transaction Id',max_length=200,null=True,blank=True)
    amount = models.IntegerField(name='amount',verbose_name='Amount',null=True,blank=True)
    reason = models.CharField(name='reason',verbose_name='Reason',max_length=300)
    created = models.DateTimeField(name='created',verbose_name='Created',auto_now_add=True)

    def toJson(self):
        return {
            'message': self.message,
            'name': self.name,
            'sender': self.sender,
            'number': self.number,
            'transactionId': self.transactionId,
            'amount': self.amount,
            'created': self.created
        }

    class Meta:
        db_table = 'invalid_payments'
        verbose_name = 'Invalid Payments'


