from django.conf.urls import url
from . import views

app_name = "custom"

urlpatterns = [
    url('^login$', views.ValidatePhoneSendOTP.as_view(), name='login'),
    url('^login/(?P<phone>.+)/$', views.OTP.as_view(), name="otp"),
    url('^signup$', views.Signup.as_view(), name='signup'),
]
