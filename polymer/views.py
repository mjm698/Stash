import json
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from datetime import datetime
from polymer.models import *

def home(request):
    return render_to_response('index.html', {}, RequestContext(request))

def stash(request):
    if 'HTTP_USER_CLIENT' in request.META:
        email = 'maxwell.mosley@gmail.com'
    else:
        email = 'maxwell.mosley@gmail.com'
    if request.method == "GET":
        thisUser = User.objects.get(email=email)
        return HttpResponse(status=200, content_type='application/json',
                            content=render(request, 'stashes.json', {'stashes': Stash.objects.filter(users=thisUser)}))


        
