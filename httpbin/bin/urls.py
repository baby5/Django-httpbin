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
    url(r'^status/(?P<code>[0-9\,]+)$', views.status, name='status'),
    url(r'^response-headers$', views.response_headers, name='response-headers'),
    url(r'^redirect/(?P<times>[0-9]+)$', views.redirect, name='redirect'),
    url(r'^redirect-to$', views.redirect_to, name='redirect-to'),
    url(r'^relative-redirect/(?P<times>[0-9]+)$', views.relative_redirect, name='relative-redirect'),
    url(r'^absolute-redirect/(?P<times>[0-9]+)$', views.absolute_redirect, name='absolute-redirect'),
    url(r'cookies$', views.cookies, name='cookies'),
    url(r'cookies/set$', views.cookies_set, name='cookies-set'),
    url(r'cookies/delete$', views.cookies_delete, name='cookies-delete'),
    url(r'basic-auth/(?P<user>.*)/(?P<passwd>.*)$', views.basic_auth, name='basic-auth'),
    url(r'hidden-basic-auth/(?P<user>.*)/(?P<passwd>.*)$', views.hidden_basic_auth, name='hidden-basic-auth'),
    url(r'digest-auth/(?P<qop>.*)/(?P<user>.*)/(?P<passwd>.*)/(?P<algorithm>.*)$', views.digest_auth, name='digest-auth'),
]
