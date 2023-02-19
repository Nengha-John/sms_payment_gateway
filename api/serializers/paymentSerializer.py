from rest_framework import serializers
from payments.models import Payment, InvalidPayments

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
    
class InvalidPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvalidPayments
        fields = '__all__'