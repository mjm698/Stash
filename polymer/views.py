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
        newBody = json.loads(request.body)

        if("stashID" in newBody):
            return deleteStash(request, newBody["stashID"])
        
        time = newBody["time"]
        name = newBody["stashName"]
        stash,created = Stash.objects.get_or_create(owner = thisUser, name = name)
        if created:
            stash.time = time
            stash.save()
            userEmails = newBody["users"]
            users = [thisUser]
            for email in userEmails:
                user = User.objects.get(email=email)
                users.append(user)
            stash.users.add(*users)
        return HttpResponse(status=200, content_type='application/json',
                            content=render(request, 'stash.json', {'stash': stash}))

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

def deleteStash(request, stashID):
    stash = Stash.objects.get(pk=stashID)
    stash.delete()
    stash.id = stashID
    return HttpResponse(status=200, content_type='application/json',
                        content=render(request, 'stash.json', {'stash': stash}))
