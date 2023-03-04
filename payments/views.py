from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http.request import HttpRequest
from datetime import datetime, timedelta
from payments.models import Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
# @login_required(login_url='/auth/login')
def home(request:HttpRequest):
    if request.user.is_authenticated:
        payment = Payment.objects.filter(user=request.user).order_by('-created')
        if payment.exists():
            payment = payment.first()
            return render(request,'pay.html',{'isSubscribed': payment.due_date.timestamp() > datetime.now().timestamp()})
    return render(request,'pay.html')

@login_required(login_url='/auth/login')
def verifyPayment(request:HttpRequest):
    if request.POST:
        transactionId = request.POST.get('transactionId')
        payment = Payment.objects.filter(transactionId=transactionId)
        if not payment.exists():
            messages.error(request,'Muamala haujathibitishwa. Tafadhali rejea namba ya muamala kisha jaribu tena')
            return render(request,'verify.html')
        payment = payment.first()
        if payment.is_valid:
            if payment.due_date.timestamp() > datetime.now().timestamp():
                messages.info(request,'Malipo yako yameshakamilishwa. Huduma yako ipo hadi {}'.format(payment.due_date.strftime('%d %b %Y')))
                return redirect('/')
            messages.error(request,'Namba ya Muamala ni Batili')
            return render(request,'verify.html')
        due_date = datetime.now() + timedelta(days=30)
        payment.is_valid = True
        payment.due_date = due_date
        payment.user = request.user
        payment.save()
        messages.info(request,'Malipo yamethibitishwa!')
        return redirect('/')
    elif request.method == 'GET':
        return render(request,'verify.html')
    return redirect(request.path)
        