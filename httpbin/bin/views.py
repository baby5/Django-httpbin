from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.template import loader
from django.views.decorators.gzip import gzip_page 

from urllib import unquote
import json
import zlib
import random


JSON_FORMAT = {
    'indent': 2,
    'sort_keys': True,
}


def home(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    return render(request, 'bin/index.html')


def ip(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    ip = request.META['REMOTE_ADDR']
    #return HttpResponse(json.dumps({'origin': ip}, indent=2), content_type='application/json')
    return JsonResponse({'origin': ip}, json_dumps_params=JSON_FORMAT)


def user_agent(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    user_agent= request.META['HTTP_USER_AGENT']
    return JsonResponse({'user-agent': user_agent}, json_dumps_params=JSON_FORMAT)


def get_headers(request):
    headers = {}
    for key, value in request.META.iteritems():#use iterator
        if key.startswith('HTTP_'):
            headers['-'.join(key.split('_')[1:]).title()] = value
        elif key.startswith('CONTENT'):
                headers['-'.join(key.split('_')).title()] = value
    return headers    


def headers(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    headers = get_headers(request)
    return JsonResponse({'headers': headers}, json_dumps_params=JSON_FORMAT)


def get(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    rep_dict = {
        'args': request.GET,
        'headers': get_headers(request),
        'origin': request.META['REMOTE_ADDR'],
        'url': request.build_absolute_uri(),
    }
    return JsonResponse(rep_dict, json_dumps_params=JSON_FORMAT)


def no_get(request, method):
    if request.method != method: return HttpResponseNotAllowed([method, 'OPTIONS'], 'Method Not Allow')
    rep_dict = {
        'args': request.GET,
        'data': request.body,
        'files': request.FILES,
        'form': request.POST,
        'headers': get_headers(request),
        'json': None,
        'origin': request.META['REMOTE_ADDR'],
        'url': request.build_absolute_uri(),
    }
    if 'json' in request.content_type:
        try:
            rep_dict['json'] = json.loads(request.body)
        except:
            pass
    return JsonResponse(rep_dict, json_dumps_params=JSON_FORMAT)


def post(request):
    return no_get(request, 'POST')


def patch(request):
    return no_get(request, 'PATCH')


def put(request):
    return no_get(request, 'PUT')


def delete(request):
    return no_get(request, 'DELETE')


def utf8(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    return render(request, 'bin/utf8.html')


@gzip_page
def gzip(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'HEAD', 'OPTIONS'], 'Method Not Allow')
    rep_dict = {
        'deflated': True,
        'headers': get_headers(request),
        'method': request.method,
        'origin': request.META['REMOTE_ADDR'],
    }
    return JsonResponse(rep_dict, json_dumps_params=JSON_FORMAT)
   

def deflate(request):
    if request.method != 'GET': return HttpResponseNotAllowed(['GET', 'OPTIONS'], 'Method Not Allow')
    rep_dict = {
        'deflated': True,
        'headers': get_headers(request),
        'method': request.method,
        'origin': request.META['REMOTE_ADDR'],
    }
    data = zlib.compress(json.dumps(rep_dict, **JSON_FORMAT))[2:-4]#2-byte zlib header and 4-byte checksum
    rep = HttpResponse(data, content_type='application/json')
    rep['Content-Encoding'] = 'deflate'
    rep['Content-Length'] = len(data)
    return rep


def status(request, code):
    code = random.choice(code.split(','))
    if code == '418':
        rep = HttpResponse(status=int(code), reason="I'M A TEAPOT")
        rep.content = loader.render_to_string('bin/418.html', request=request)
        del rep['content-type']
        return rep
    return HttpResponse(status=int(code))


def response_headers(request):
    rep = HttpResponse(content_type='application/json')
    headers = {k: v for k, v in rep.items()}
    headers['Content-Length'] = ''
    if request.META['QUERY_STRING']:
        query_string_list = [qs.split('=', 1) for qs in unquote(request.META['QUERY_STRING']).split('&')]
        for k, v in query_string_list:
            rep[k] = v
            if k not in headers:
                headers[k] = v
            else:
                if isinstance(headers[k], list):
                    headers[k].append(v)
                else:
                    headers[k] = [headers[k], v]
    length = len(json.dumps(headers, **JSON_FORMAT))
    headers['Content-Length'] = str(length+len(str(length)))
    rep['Content-Length'] = headers['Content-Length']
    rep.content = json.dumps(headers, **JSON_FORMAT)
    return rep


def redirect(request, times):
    if times == '1':
        return HttpResponseRedirect(reverse('get'))
    else:
        return HttpResponseRedirect(reverse('redirect', args=[int(times)-1]))
