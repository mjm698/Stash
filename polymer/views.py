import json
import requests
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from polymer.models import *

@login_required(login_url='/login/')
def home(request):
    return render_to_response('index.html', {}, RequestContext(request))

@login_required(login_url='/login/')
@csrf_exempt
def stash(request):
    thisUser = request.user
    if request.method == "GET":
        stashes = Stash.objects.filter(users = thisUser)
        previousStash = PreviousStash.objects.get_or_none(user = thisUser)
        return HttpResponse(status=200, content_type='application/json',
                content=json.dumps({'stashes' : [s.to_json() for s in stashes],
                                    'prevStash' : 0 if (previousStash == None) else previousStash.to_json()}, 
                                    ensure_ascii=False))
    elif request.method == "POST":
        newBody = json.loads(request.body)

        if "stashID" in newBody:
            return deleteStash(request, newBody["stashID"])
        else:
            return createStash(request, newBody, thisUser)
        
@login_required(login_url='/login/')
@csrf_exempt
def comment(request):
    if request.method == "POST":
        newBody = json.loads(request.body, strict = False)
        thisUser = request.user
        text = newBody["text"]
        time = datetime.datetime.now()
        comment,created = Comment.objects.get_or_create(user = thisUser, content_id = newBody["contentId"], text = text, time = time)
        if created:
            return HttpResponse(status=200, content_type='application/json',
                                content=json.dumps(comment.to_json(), ensure_ascii=False))
        else:
            return returnEmpty(request)

@login_required(login_url='/login/')
@csrf_exempt
def content(request):
    thisUser = request.user

    if request.method == "GET":
        stashId = request.META['HTTP_STASHID']
        contents = Content.objects.filter(stash_id = stashId)
        return HttpResponse(status=200, content_type='application/json',
                            content=json.dumps([c.to_json(thisUser) for c in contents], ensure_ascii=False))

    elif request.method == "POST":
        newBody = json.loads(request.body)
        if 'stashId' not in newBody:
            return HttpResponse(status=400)
        content = createContent(thisUser, datetime.datetime.now(), newBody['link'], newBody['stashId'], newBody['title'], newBody['content'])
        if content:
            return HttpResponse(status=200, content_type='application/json',
                                content=json.dumps(content.to_json(thisUser), ensure_ascii=False))
        else:
            return returnEmpty(request)

@login_required(login_url='/login/')
@csrf_exempt
def update(request):
    thisUser = request.user

    if request.method == "POST":
        newBody = json.loads(request.body)
        if "type" not in newBody:
            return HttpResponse(status=400)
        else:
            updateType = newBody['type']
        if "contentId" not in newBody:
            return HttpResponse(status=400)
        else:
            contentId = newBody['contentId']
        content = Content.objects.get(pk=contentId)
        if updateType == "delete":
            content.delete()
        else:
            status = Status.objects.filter(user= thisUser).get(content = content)
            if updateType == 'archive':
                status.status = Status.ARCHIVED_STATUS
            elif updateType == "view":
                status.status = Status.VIEWED_STATUS
            status.save()
        return HttpResponse(status=200)

@login_required(login_url='/login/')
@csrf_exempt
def user(request):
    if request.method == "POST":
        newBody = json.loads(request.body)
        username = newBody['username']
        try:
            user = User.objects.get(username = username)
        except:
            user = None
        if user == None:
            return returnEmpty(request)
        else:
            data = { 'id':user.id,
                     'name':user.get_username()}
            return HttpResponse(status=200, content_type='application/json',
                                 content=json.dumps({'id':user.id, 'name':user.get_username()}, ensure_ascii=False))

@login_required(login_url='/login/')
@csrf_exempt
def view(request):
    return render(request, 'view.html')

@login_required(login_url='/login/')
@csrf_exempt
def viewContent(request):
    user = request.user
    contentId = request.META['HTTP_CONTENTID']
    content = Content.objects.get(pk=contentId)
    return HttpResponse(status=200, content_type='application/json',
                        content=json.dumps(content.to_json(user), ensure_ascii=False))

@csrf_exempt
def stashName(request):
    thisUser = request.user
    if request.method == "POST":
        newBody = json.loads(request.body)
        stashId = newBody["stashID"]
        stashName = newBody["newStashName"]
        stash = Stash.objects.get(pk=stashId)
        stash.name = stashName
        stash.save()
        return HttpResponse(status=200, content_type='application/json',
                             content=json.dumps({'stashID':stash.id, 'stashName':stash.name}, ensure_ascii=False))

@login_required(login_url='/login/')
@csrf_exempt
def parse(request):
    thisUser = request.user
    newBody = json.loads(request.body)
    link = newBody["link"]
    stashId = newBody["stashId"]
    fullUrl = 'https://readability.com/api/content/v1/parser?url=' + link + '&token=8a61b740a6767f2c33728cc19f87e7f817cb1c39'
    r = requests.get(fullUrl)
    responseBody = json.loads(r.text)
    if 'error' in responseBody:
        return HttpResponse(status=200, content_type='application/json', content=json.dumps({'error':'True', 'message':responseBody['messages'], 'link':link}, ensure_ascii=False))
    else:
        content = createContent(thisUser, datetime.datetime.now(), responseBody['url'], stashId, responseBody['title'], responseBody['content'])
        return HttpResponse(status=200, content_type='application/json',
                            content=json.dumps(content.to_json(thisUser), ensure_ascii=False))

def createStash(request, newBody, thisUser):
        name = newBody["stashName"]
        userIds = newBody["users"]
        users = [thisUser]
        for userId in userIds:
            user = User.objects.get(pk=userId)
            users.append(user)
        stash = createNewStash(thisUser, name, users)
        if stash:
            return HttpResponse(status=200, content_type='application/json',
                                content=json.dumps(stash.to_json(), ensure_ascii=False))
        else:
            return returnEmpty(request)

def createContent(thisUser, time, link, stashId, title, content):
    content,created = Content.objects.get_or_create(user = thisUser, time = time, link = link, stash_id = stashId, updateTime = time, title = title, content = content)
    if created:
        createStati(content, stashId)
        return content
    else:
        return None

def createStati(content, stashId):
    thisStash = Stash.objects.get(pk=stashId)
    for user in thisStash.users.all():
        Status(user = user, content = content, status = Status.NEW_STATUS).save()

def returnEmpty(request):
    return HttpResponse(status=200, content_type='application/json',
                        content=render(request, 'empty.json'))

def deleteStash(request, stashID):
    stash = Stash.objects.get(pk=stashID)
    stash.delete()
    stash.id = stashID
    return HttpResponse(status=200, content_type='application/json',
                        content=render(request, 'stash.json', {'stash': stash}))

def createNewStash(user, name, users):
    stash,created = Stash.objects.get_or_create(owner = user, name = name)
    if created:
        prev,prevCreated = PreviousStash.objects.get_or_create(user = user)
        if prevCreated:
            prev.stash = stash
            prev.save()
        stash.time = datetime.datetime.now()
        stash.save()
        prev,prevCreated = PreviousStash.objects.get_or_create(user = user)
        if prevCreated:
            prev.stash = stash
            prev.save()
        stash.time = datetime.datetime.now()
        stash.save()
        stash.users.add(*users)
        return stash
    else:
        return None

def createDefaultStash(user):
    name = (user.get_username() + "'s Stash")
    users = [user]
    stash = createNewStash(user, name, users)
    time = datetime.datetime.now()
    stashId = stash.id
    link = "default"
    title = "Welcome to Stash."
    content = "You can add a new link by clicking the plus in the top right. Create a new stash by opening your stash list and clicking the plus."
    createContent(user, time, link, stashId, title, content)
