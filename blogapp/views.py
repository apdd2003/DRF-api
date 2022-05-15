from urllib import request
from wsgiref.util import request_uri
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import BlogPost
from . import serializers
from rest_framework.response import Response

from rest_framework import generics, permissions


from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate



def index(request, path=''):
    return render(request, 'index.html')
 
class UserViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the User model
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
    # serializer holds a django model
        serializer.save(user=self.request.user)
 
class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the Blog Post model
    """
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # def retrieve(self, request, *args, **kwargs):
    #     return Response({'something': 'my custom JSON'})
 
    def destroy(self,*args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # print('update request received')
        req_url = self.request.build_absolute_uri()
        post_id = req_url.split('/')[-1]
        postuser = BlogPost.objects.filter(id=post_id).all()[0].user
        # print(postuser)
        # print(post_id)
        if(postuser==self.request.user):
            serializer.save()
        else:
            
            # print('Not authorized to update')
            return Response(
                {'error': 'you are not authorized to update this post'},400)
        # return Response(serializer.data)
        return Response({'message': 'Post Deleted'}, 204)


    def delete(self,*args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # print('update request received')
        req_url = self.request.build_absolute_uri()
        post_id = req_url.split('/')[-1]
        postuser = BlogPost.objects.filter(id=post_id).all()[0].user
        # print(postuser)
        # print(post_id)
        if(postuser==self.request.user):
            serializer.save()
        else:
            
            # print('Not authorized to update')
            return Response(
                {'error': 'you are not authorized to delete this post'},400)
        return Response(serializer.data)



    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)




@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
        request,
        username=data['username'],
            password=data['password'])
        if user is None:
            return JsonResponse(
            {'error':'unable to login. check username and password'},
            status=400)
        else: # return user token
            try:
                token = Token.objects.get(user=user)    
            except: # if token not in db, create a new one
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error': 'username already taken.'},
                status=400)


def register(request):
    return render(request,'register.html')