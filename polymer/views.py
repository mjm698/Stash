import json
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from polymer.models import *

def home(request):
    return render_to_response('index.html', {}, RequestContext(request))

@csrf_exempt
def stash(request):
    if 'HTTP_USERID' in request.META:
        userId = request.META['HTTP_USERID']
    else:
        userId = '1'
    thisUser = User.objects.get(pk=userId)
    if request.method == "GET":
        stashes = Stash.objects.filter(users = thisUser)
        return HttpResponse(status=200, content_type='application/json',
                            content=json.dumps([s.to_json() for s in stashes], ensure_ascii=False))
    elif request.method == "POST":
        newBody = json.loads(request.body)

        if("stashID" in newBody):
            return deleteStash(request, newBody["stashID"])
        
        name = newBody["stashName"]
        stash,created = Stash.objects.get_or_create(owner_id = userId, name = name)
        if created:
            stash.time = datetime.datetime.now()
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
            return returnEmpty()

def comment(request):
    if request.method == "POST":
        newBody = json.loads(request.body)
        userId = newBody["userId"]
        text = newBody["text"]
        time = datetime.datetime.now()
        comment,created = Comment.objects.get_or_create(user_id = newBody["userId"], content_id = newBody["contentId"], text = text, time = time)
        if(created):
            return HttpResponse(status=200, content_type='application/json',
                                content=json.dumps(comment.to_json(), ensure_ascii=False))
        else:
            return returnEmpty()

def content(request):
    #todo: remove email and use user object instead
    if 'HTTP_USERID' in request.META:
        userId = request.META['HTTP_USERID']
    else:
        userId = 1
    thisUser = User.objects.get(pk=userId)

    if 'HTTP_STASHID' in request.META:
        stashId = request.META['HTTP_STASHID']
    else:
        stashId = 421412

    if request.method == "GET":
        contents = Content.objects.filter(stash_id = stashId)
        return HttpResponse(status=200, content_type='application/json',
                            content=json.dumps([c.to_json(thisUser) for c in contents], ensure_ascii=False))
    elif request.method == "POST":
        newBody = json.loads(request.body)
        if('stashId' not in newBody):
            return HttpResponse(status=400)
        stashId = newBody['stashId']
        link = newBody['link']
        time = datetime.datetime.now()
        content,created = Content.objects.get_or_create(user_id = userId, time = time, link = link, stash_id = stashId, updateTime = time)
        if(created):
            createStati(content, stashId)
            return HttpResponse(status=200, content_type='application/json',
                                content=json.dumps(content.to_json(thisUser), ensure_ascii=False))
        else:
            return returnEmpty()

def update(request):
    #todo: remove email and use user object instead
    if 'HTTP_USERID' in request.META:
        userId = request.META['HTTP_USERID']
    else:
        userId = 1

    if request.method == "POST":
        newBody = json.loads(request.body)
        if("type" not in newBody):
            return HttpResponse(status=400)
        if("contentId" not in newBody):
            return HttpResponse(status=400)
        else:
            contentId = newBody['contentId']
        content = Content.objects.get(pk=contentId)
        if(newBody['type'] == "delete"):
            content.delete()
        else:
            status = Status.objects.filter(user_id = userId).get(content = content)
            if(newBody['type'] == 'archive'):
                status.status = Status.ARCHIVED_STATUS
            elif(newBody['type']) == "view":
                status.status = Status.VIEWED_STATUS
            status.save()
        return HttpResponse(status=200)

def createStati(content, stashId):
    thisStash = Stash.objects.get(pk=stashId)
    for user in thisStash.users.all():
        Status(user = user, content = content, status = Status.NEW_STATUS).save()


def returnEmpty():
    return HttpResponse(status=200, content_type='application/json',
                        content=render(request, 'empty.json'))

def deleteStash(request, stashID):
    stash = Stash.objects.get(pk=stashID)
    stash.delete()
    stash.id = stashID
    return HttpResponse(status=200, content_type='application/json',
                        content=render(request, 'stash.json', {'stash': stash}))
