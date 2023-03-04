
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
import re
from datetime import datetime
from payments.models import Payment,InvalidPayments
from rest_framework import generics
from api.serializers.paymentSerializer import PaymentSerializer,InvalidPaymentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 250
    page_query_param = 'page'



@api_view(['POST'])
@csrf_exempt
def processPayment(request:Request):
        data = request.data
        message = data['message']
        sender = data['from']
        reasons = []
        number = ''
        name = ''
        amount = ''
        transactionId = ''
        print('New Message')
        if 'Umelipa' in message:
            print(message)
            pass
        elif sender.lower() == 'airtelmoney':
            print('Matching Message: ',data)
            amount = re.search(r'\D*\d{1,3}(,\d{3})*',message)
            if amount:
                amount = re.sub(r'\D', '', amount.group())
            else:
                reasons.append('Amount could not be parsed')
            transactionId = re.search(r'Muamala No\.(.+)',message)
            number = re.search(r'\d{9}',message)
            name = re.search(r"kutoka ([A-Z ]+)",message)
            if not transactionId:
                reasons.append('Could not parse Transaction Id')
            else:
                transactionId =  transactionId.group(1).replace(':','').strip()
            if number:
                number = number.group()
            if name:
                name = name.group(1)
            if int(amount) != 2000:
                reasons.append('Invalid Amount')
           
        elif sender.lower() == 'm-pesa':
            transactionId = re.search(r'(\w+)\s+Imethibitishwa',message)
            if transactionId:
                transactionId = transactionId.group(1)
            else:
                 reasons.append('Could not parse Transaction Id')
            amountAndPhoneName = re.search(r'\bTsh([\d,]+\.\d{2})\b.*?\b(\d{12})\b - \b([A-Z ]+)\b',message)
            if amountAndPhoneName:
                amount = int(amountAndPhoneName.group(1))
                if not amount:
                     reasons.append('Could not parse amount')
                number = amountAndPhoneName.group(2)
                name = amountAndPhoneName.group(3)
        elif sender.lower() == 'tigopesa':
            transactionId = re.search(r'KumbukumbuNo\.: (\d+)',message)
            if transactionId:
                transactionId = transactionId.group(1)
            else:
                 reasons.append('Could not parse Transaction Id')
            amountAndPhoneName = re.search(r'\bTSh\s*([\d,]+\.\d+)\b.*? \b(\d{12})\b - \b([A-Z ]+)\b',message)
            if amountAndPhoneName:
                amount = amountAndPhoneName.group(1)
                if not amount:
                    reasons.append('Could not parse Amount')
                number = amountAndPhoneName.group(2)
                name = amountAndPhoneName.group(3)
        else:
            print(message)
        if len(reasons) != 0:
                print(sender, amount, transactionId, number, name)
                pay = InvalidPayments.objects.create(message=message,name=name,sender=sender,number=number,amount=amount, transactionId=transactionId,reason=', '.join(reasons))
          
        else:
                print(sender, amount, transactionId, number, name)
                pay = Payment.objects.create(message=message,name=name, sender=sender,number=number,transactionId=transactionId,amount=amount) 
        return Response(status=200)


class PaymentList(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class =  PaymentSerializer
    queryset = Payment.objects.all().order_by('-created')


class InvalidPaymentList(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = InvalidPaymentSerializer
    queryset = InvalidPayments.objects.all().order_by('-created')