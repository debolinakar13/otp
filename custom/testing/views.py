import random
import time
import hashlib

from django_otp.oath import totp
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from rest_framework.reverse import reverse

from .forms import UserCreationForm, AuthenticationForm, OTPForm
from twilio.rest import Client
from .models import User

class ValidatePhoneSendOTP(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    
    def get(self, request):
        form = AuthenticationForm()
        return Response({'form':form}, template_name='login.html')

    def post(self, request):
        if 'phone' in request.data:
            phone_number = request.POST.getlist('phone')[0]
            user = User.objects.filter(phone=phone_number)
            new = User.objects.all()
            if user.exists():
                phone_number = str(phone_number)
                key = self.send_otp(phone_number)
                account_sid = 'AC8917ff1d48e84f56e6ce5b810b662264'
                auth_token = 'd7e6f4cd7c38a1f759da17e6de07b8e2'
                if key:
                    client = Client(account_sid, auth_token)
                    client.messages.create(
                        to='+91'+ phone_number,
                        from_='+13044704723',
                        body='Your One Time Password is '+str(key))
                    new.otp = key
                    new.update(otp=key)
                    #new.save()
                    return redirect('custom:otp', phone_number)
            else:
                form = UserCreationForm() 
                return Response({'form':form}, template_name='not_logged_in.html')

    def send_otp(self, phone):
        key = random.randint(0, int(phone))
        now = int(time.time())
        for delta in range(0, 200, 20):
            key = totp(str(key), t0=(now-delta))
            return key

class OTP(APIView):

    renderer_classes = (TemplateHTMLRenderer,JSONRenderer)
    
    def get(self, request, phone):
        self.phone = phone
        form = OTPForm()
        return Response({'form':form}, template_name='otp.html')

    def post(self, request, phone):
        self.phone = phone
        otp = request.data.get('otp')
        user = User.objects.all().first()
        old_otp = User.objects.values_list('otp').filter(phone=self.phone).first()[0]
        if int(otp)==old_otp:
            login(request, user)
            return redirect('custom:signup')
        else:
            form = OTPForm()
            return Response({'form':form}, template_name='otp.html')

class Signup(APIView):
    
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        form = UserCreationForm()
        return Response({'form':form}, template_name='signup.html')

    def post(self, request):
        form = UserCreationForm(request.POST)
        phone = request.data.get('phone')
        email = request.data.get('email')
        if form.is_valid():
            user = form.save()
            authenticate(phone=phone, email=email)
            return redirect('custom:login')
	else:
    	    form = UserCreationForm()
            return Response({'form':form}, template_name='signup.html')
