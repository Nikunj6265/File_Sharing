from django.http import JsonResponse,HttpResponse
from app_api.models import Client, File
from django.shortcuts import redirect
from django.contrib.auth.models import User
import uuid
from django.http import FileResponse
import os
from rest_framework import generics
from .serializers import UserSerializer, FileSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def verify(request , auth_token):
    try:
        profile_obj = Client.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                return JsonResponse({'Already':'Your account is already verified.'})
            profile_obj.is_verified = True
            profile_obj.save()
            return JsonResponse({'Successfull':'Your account is verified.'})
        else:
            return JsonResponse({'Invalid':'Account.'})
    except Exception as e:
        print(e)
    return HttpResponse('Please make a correct request')


@csrf_exempt
def ClientSignUp(request):
    if request.method == 'POST':

        Jsondata = JSONParser().parse(request)
        
        serializer = UserSerializer(data = Jsondata)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                if User.objects.filter(username = username).first():
                    return JsonResponse({'Already':'Username is taken.'})
                

                if User.objects.filter(email = email).first():
                    return JsonResponse({'Already':'Email is taken.'})
            
            
                user_obj = User.objects.create_user(username=username, email=email, password=password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                
                profile_obj = Client.objects.create(user = user_obj , auth_token = auth_token)
                profile_obj.save()
                send_mail_after_registration(email , auth_token)
                return JsonResponse({'Successfully':'Email is sent.'})

            except Exception as e:
                print(e)  
    return HttpResponse('Please make a post request')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

  

class home(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()

@csrf_exempt
def login_attempt(request):
    if request.method == 'POST':
            Jsondata = JSONParser().parse(request)

            username = Jsondata['username']
            password = Jsondata['password']

            user_obj = User.objects.filter(username = username).first()
            if user_obj is None:
                return JsonResponse({'Error':'User not found.'})
        
            profile_obj = Client.objects.filter(user = user_obj).first()

            if not profile_obj.is_verified:
                return JsonResponse({'Exception':'Profile is not verified check your mail.'})
            

            user = authenticate(request, username = username , password = password)
            if user is None:
                return JsonResponse({'Exception':'Wrong password'})
        
            login(request , user)
            return redirect('home/')

    return HttpResponse('please make a post request for login first')

@login_required
def download(request, filename):
    f = 'uploads/'+filename
    file = os.path.join(settings.BASE_DIR,f)
    print(file)
    fileOpened = open(file, 'rb')
    print(FileResponse(fileOpened))
    return FileResponse(fileOpened)