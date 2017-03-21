from functools import wraps
import json

from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils.decorators import available_attrs


def methods(method_list):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kw):
            if request.method not in method_list:
                return HttpResponseNotAllowed(method_list, 'Method Not Allow')
            return func(request, *args, **kw)
        return inner
    return decorator



def get_headers(request):
    headers = {}
    for key, value in request.META.iteritems():#use iterator
        if key.startswith('HTTP_'):
            headers['-'.join(key.split('_')[1:]).title()] = value
        elif key.startswith('CONTENT'):
                headers['-'.join(key.split('_')).title()] = value
    return headers    


def no_get(request):
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
    return rep_dict
