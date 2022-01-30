import re

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        if re.match('^/home/', path):
            if request.session.get('user', '') == '':
                return HttpResponseRedirect(reverse('please'))
        if re.match('^/sellers/', path):
            if request.session.get('seller', '') == '':
                return HttpResponseRedirect(reverse('pleases'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response