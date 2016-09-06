# Create your views here.
from django.shortcuts import render_to_response
from django.views.generic import View


class LoginView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render_to_response('login.html')
        return response
