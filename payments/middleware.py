from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.conf import settings
class APIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request:HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        allowed = ['/api/login','/api/register','/api/sub/process']
        if request.path in allowed:
            pass
        elif '/api/' in request.path:
            key = ''
            if request.method == 'GET':
                key = request.GET.get('api_key')
            elif request.method == 'POST':
                key = request.POST.get('api_key')
            if not key or key not in settings.CUSTOM_API_KEYS:
                return HttpResponse('Unauthorized',status=403)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response