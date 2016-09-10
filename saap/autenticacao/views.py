# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext


class LoginView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.user.is_authenticated():
            response = redirect('/')
        else:
            response = render_to_response('login.html', context=RequestContext(request))
        return response

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                # Message
                return redirect('/')
            #else:
                # Message
        #else:
            # Message
        
        return render_to_response('login.html', context=RequestContext(request))
