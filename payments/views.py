from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http.request import HttpRequest
from datetime import datetime, timedelta
from payments.models import Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/auth/login')
def home(request:HttpRequest):
    return render(request,'home.html')

@login_required(login_url='/auth/login')
def verifyPayment(request:HttpRequest):
    if request.POST:
        transactionId = request.POST.get('transactionId')
        payment = Payment.objects.filter(transactionId=transactionId)
        if not payment.exists():
            messages.error(request,'Transaction Not Found. Please cross check your entry and try again')
            return render(request,'verify.html')
        payment = payment.first()
        if payment.is_valid:
            messages.error(request,'Invalid Transaction ID')
            return render(request,'verify.html')
        due_date = datetime.now() + timedelta(days=30)
        payment.is_valid = True
        payment.due_date = due_date
        payment.user = request.user
        payment.save()
        messages.info(request,'Payment Verified Successfully')
        return redirect('/')
    elif request.method == 'GET':
        return render(request,'verify.html')
    return redirect(request.path)
        