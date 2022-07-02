from django.shortcuts import render
import random
from rest_framework.response import Response

# Create your views here.
from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer

class PostAPIView(generics.ListAPIView):
    def get(self, *args, **kwargs):
        queryset = Post.objects.all()
        random_word = random.choice(queryset)
        serializer_class = PostSerializer(random_word)
        return Response(serializer_class.data)