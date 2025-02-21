from rest_framework import serializers
from .models import Blog, Comment

class CommemtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class BlogSerializer(serializers.ModelSerializer):
    comments = CommemtSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'