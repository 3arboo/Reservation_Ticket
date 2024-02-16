from rest_framework import serializers
from Ticket.models import Geust , Movie , Resrvation ,Post

class GeustSerializers(serializers.ModelSerializer):
    class Meta:
        model = Geust
        fields = '__all__'
class MovieSerilazers(serializers.ModelSerializer):
    class Meta :
        model = Movie
        fields = '__all__'

class ResrvationSerializers(serializers.ModelSerializer):
    class Meta:
        model= Resrvation
        fields= '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'