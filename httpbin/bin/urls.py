"""httpbin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^ip$', views.ip, name='ip'),
    url(r'^user-agent$', views.user_agent, name='user-agent'),
    url(r'^headers$', views.headers, name='headers'),
    url(r'^get$', views.get, name='get'),
    url(r'^post$', views.post, name='post'),
    url(r'^patch$', views.patch, name='patch'),
    url(r'^put$', views.put, name='put'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^encoding/utf8$', views.utf8, name='utf8'),
    url(r'^gzip$', views.gzip, name='gzip'),
    url(r'^deflate$', views.deflate, name='deflate'),
]
