from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.core import serializers
from django.views.decorators.gzip import gzip_page 

import json
import zlib


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
