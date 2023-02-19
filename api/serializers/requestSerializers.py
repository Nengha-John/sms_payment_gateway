from rest_framework import serializers
from ng_requests.models import MovieRequest,ShowRequest

class MovieRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model= MovieRequest
        fields = "__all__"
    
class ShowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowRequest
        fields = '__all__'