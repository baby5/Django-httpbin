from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

import json


JSON_FORMAT = {
    'indent': 2,
    'sort_keys': True,
}


def home(request):
    return render(request, 'bin/index.html')


def ip(request):
    ip = request.META['REMOTE_ADDR']
    #return HttpResponse(json.dumps({'origin': ip}, indent=2), content_type='application/json')
    return JsonResponse({'origin': ip}, json_dumps_params=JSON_FORMAT)


def user_agent(request):
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
    headers = get_headers(request)
    return JsonResponse({'headers': headers}, json_dumps_params=JSON_FORMAT)


def get(request):
    rep_dict = {}
    rep_dict['args'] = request.GET
    rep_dict['headers'] = get_headers(request)
    rep_dict['origin'] = request.META['REMOTE_ADDR']
    rep_dict['url'] = request.build_absolute_uri()
    return JsonResponse(rep_dict, json_dumps_params=JSON_FORMAT)


def post(request):
    if request.method != 'POST':
        rep = HttpResponse('Method Not Allowed', status=405)
        rep['Allow'] = 'POST, OPTIONS'
        return rep
    rep_dict = {}
    rep_dict['args'] = request.GET
    rep_dict['data'] = request.body
    rep_dict['files'] = request.FILES
    rep_dict['form'] = request.POST
    rep_dict['headers'] = get_headers(request)
    rep_dict['json'] = None
    if 'json' in request.content_type:
        try:
            rep_dict['json'] = json.loads(request.body)
        except:
            pass
    rep_dict['origin'] = request.META['REMOTE_ADDR']
    rep_dict['url'] = request.build_absolute_uri()
    return JsonResponse(rep_dict, json_dumps_params=JSON_FORMAT)
   
