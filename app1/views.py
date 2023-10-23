from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.db.models import Count
from . serializer import *
from . models import *
import uuid, time, os
from qrcode import *
from django.conf import settings
# Create your views here.


class User_regiter(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        print(request.data)
        
        if "first_name" not in request.data:
            raise APIException("all fields are required......!!")
 
        if 'email' in request.data:
            if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', request.data['email']):

                raise APIException("Email is not correct")
 
            if 'password' in request.data:
                if not re.match(r'^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z\d]{8,}$', request.data['password']):  
                    raise APIException("Password must contain at least 8 characters, including both letters and digits") 
          
        if User.objects.filter(email=request.data['email']).exists():
            raise APIException("Email is already exists")
        
        new_user = User.objects.create_user(username=request.data["first_name"] +" " + request.data["last_name"], password=request.data['password'], email=request.data['email'])
        response = {
            "status": status.HTTP_200_OK,
            "message": "User registration complate...",
           
        }
        return Response(response)
    

class user_login(generics.GenericAPIView):
    permission_classes =[AllowAny]
    def post(Self, request):
        if User.objects.filter(email=request.data['email']).exists():
            new_user = User.objects.get(email=request.data['email'])
            response = {
                "status": status.HTTP_302_FOUND,
                "message": "login sucess.....",
                "refresh_token": str(RefreshToken.for_user(user=new_user)),
                "access_token": str(AccessToken.for_user(user=new_user))

            }
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Login Failed"
            }
        return Response(response)
    

class create_shorterend_url(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):


        new_obj = shortend_url.objects.create(
            users_id = request.user,
            orginal_url = request.data['long_url'],
            shorted_url = uuid.uuid4
        )
        url = f"http://127.0.0.1:8000/create_qr?id={request.user.id}"
        img = make(url)
        image_name = 'qr' + str(time.time()) + '.png'
        img.save(os.path.join(settings.MEDIA_ROOT, image_name))

        response = {
            "status": status.HTTP_200_OK,
            "message": "sucessfully generated....",
            "long_url": new_obj.orginal_url,
            "short_url": str(new_obj.shorted_url)
        }
        return Response(response)
    


@api_view(['GET'])
def find_user(request, id):
        no_visitor = shortend_url.objects.get(users_id = id)
        no_visitor.no_of_visitor =+ 1
        no_visitor.save()
        respons = {
            "status": status.HTTP_200_OK,
            "vistiors" : no_visitor.no_of_visitor
        }
        return Response(respons)

class delete_url(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        shortend_url.objects.delete(users_id=request.user.id)
        return Response({"message":"deleted sucessfully...."})
    
class view_url(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        url = shortend_url.objects.get(uders_id=request.user.id)
        response = {
            "original_url": url.orginal_url,
            "short_url": url.shorted_url
        }
        return Response(response)    
    
class update_url(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        url = shortend_url.objects.get(uders_id=request.user.id)
        url.orginal_url = request.data['new_url']
        url.shorted_url = uuid.uuid4
        url.save()
        urls = f"http://127.0.0.1:8000/create_qr?id={request.user.id}"
        img = make(urls)
        image_name = 'qr' + str(time.time()) + '.png'
        img.save(os.path.join(settings.MEDIA_ROOT, image_name))

        response = {
            "status": status.HTTP_200_OK,
            "message": "sucessfully generated....",
            "long_url": url.orginal_url,
            "short_url": str(url.shorted_url)
        }
        return Response(response)    
    
# admin side code
class show_user_details(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        result = shortend_url.objects.values('users_id').annotate(Count("shorted_url"))    
        print(result)

        return Response(result)
    
class view_user(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        final_result = {}

        user = shortend_url.objects.all()
        for us in user:
            if us not in final_result:
                final_result[str(us)] = {
                    "username":us.users_id.username,
                    "us.users_id.username": us.users_id.email,
                    "long_url": us.orginal_url,
                    "short_url": us.shorted_url,
                    "visitor_count" : 0
                }
             
            else:
                final_result[str(us)].get('visitor_count', 0) + 1
            
                 
        return Response(final_result)        