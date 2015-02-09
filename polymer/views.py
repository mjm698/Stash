import json
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from polymer.models import *

def home(request):
    return render_to_response('index.html', {}, RequestContext(request))

@csrf_exempt
def stash(request):
    if 'HTTP_EMAIL' in request.META:
        email = request.META['HTTP_EMAIL']
    else:
        email = 'maxwell.mosley@gmail.com'
    if request.method == "GET":
        thisUser = User.objects.get(email=email)
        return HttpResponse(status=200, content_type='application/json',
                            content=render(request, 'stashes.json', {'stashes': Stash.objects.filter(users=thisUser)}))
    elif request.method == "POST":
        thisUser = User.objects.get(email=email)
        newDict = request.POST
        newBody = request.body
        time = request.POST.get("time")
        name = request.POST.get("stashName")
        userEmails = request.POST.get("users")
        users = []
        for email in userEmails:
            users.add(User.objects.get(email=email))
        stash = Stash.objects.create(owner = thisUser, time = time, name = name)
        stash.save()
        stash.users.add(users)
        return HttpResponse(status=200, content_type='application/json',
                            content=render(request, 'stashes.json', {'stashes': stash}))

def content(request):
    if 'HTTP_EMAIL' in request.META:
        email = request.META['HTTP_EMAIL']
    else:
        email = 'maxwell.mosley@gmail.com'
    if 'HTTP_STASHID' in request.META:
        stashId = request.META['HTTP_STASHID']
    else:
        stashId = 1

    if request.method == "GET":
        thisUser = User.objects.get(email=email)
        thisStash = Stash.objects.get(pk=stashId)
        return HttpResponse(status=200, content_type='application/json',
                            content=render(request, 'contents.json', {'content': Content.objects.filter(stash=thisStash)}))
