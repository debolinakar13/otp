from django.conf.urls import url, include
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('testing.urls')),
    url(r'', include(tf_urls))
]
