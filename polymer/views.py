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
        stashes = Stash.objects.filter(users = thisUser)
        return HttpResponse(status=200, content_type='application/json',
                            content=json.dumps([s.to_json() for s in stashes], ensure_ascii=False))
    elif request.method == "POST":
        thisUser = User.objects.get(email=email)
        newBody = json.loads(request.body)

        if("stashID" in newBody):
            return deleteStash(request, newBody["stashID"])
        
        time = datetime.datetime.now()
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
                                content=json.dumps(stash.to_json(), ensure_ascii=False))
        else:
            return HttpResponse(status=200, content_type='application/json',
                                content=render(request, 'empty.json'))

def content(request):
    #todo: remove email and use user object instead
    if 'HTTP_EMAIL' in request.META:
        email = request.META['HTTP_EMAIL']
    else:
        email = 'maxwell.mosley@gmail.com'
    thisUser = User.objects.get(email=email)

    #todo: figure out better way of handling else
    if 'HTTP_STASHID' in request.META:
        stashId = request.META['HTTP_STASHID']
    else:
        stashId = 1

    if request.method == "GET":
        thisStash = Stash.objects.get(pk=stashId)
        contents = Content.objects.filter(stash = thisStash)
        return HttpResponse(status=200, content_type='application/json',
                            content=json.dumps([c.to_json(thisUser) for c in contents], ensure_ascii=False))

    elif request.method == "POST":
        newBody = json.loads(request.body)
        if("type" not in newBody):
            return HttpResponse(status=400)
        if("contentID" not in newBody):
            return HttpResponse(status=400)
        else:
            contentID = newBody['contentID']
        content = Content.objects.get(pk=contentID)
        if(newBody['type'] == "delete"):
            #todo: delete the record
            return HttpResponse(status=200)
        else:
            status = Status.objects.filter(user=thisUser).get(content = content)
            if(newBody['type'] == 'archive'):
                status.status = Status.ARCHIVED_STATUS
            elif(newBody['type']) == "view":
                status.status = Status.VIEWED_STATUS
            status.save()
        return HttpResponse(status=200)


def deleteStash(request, stashID):
    stash = Stash.objects.get(pk=stashID)
    stash.delete()
    stash.id = stashID
    return HttpResponse(status=200, content_type='application/json',
                        content=render(request, 'stash.json', {'stash': stash}))
