from rest_framework import serializers
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password','groups','user_permissions']