import json
from django.shortcuts import render_to_response, redirect, RequestContext, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from polymer.models import *

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    errors = []
    if request.method == "POST":
        newBody = json.loads(request.body)
        username = newBody['username']
        password = newBody['password']
        user = authenticate(username=username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp = {'login' : True, 'user' : user.get_username(), 'errors' : []}
                return HttpResponse(status=200, content_type='application/json', 
                                    content=json.dumps(resp, ensure_ascii=False))
            else:
                errors.append({'message': "Your account has been disabled"})
                resp = {"login":False, "errors":errors}
                return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
        else:
            errors.append({'message': "The username and password you have entered do not match our records"})
            resp = {"login":False, "errors":errors}
            return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
    return render_to_response("login.html", {'errors': errors}, RequestContext(request))

@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        newBody = json.loads(request.body)
        if 'selectedStash' in newBody:
            if newBody['selectedStash'] != "":
                previousStash = PreviousStash.objects.get(user = request.user)
                selectedStash = Stash.objects.get(pk=newBody['selectedStash'])
                previousStash.stash_id = selectedStash
                previousStash.save()
        logout(request)
        resp = {"login":False}
        return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))

@csrf_exempt
def register(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    errors = []
    if request.method == "POST":
        newBody = json.loads(request.body)
        username = newBody['username']
        password = newBody['password']
        confirm = newBody['confirm']
        email = newBody['email']
        if not username:
            errors.append({'message': "You need to enter a username"})
        if not email:
            errors.append({'message': "You need to enter an email address"})
        if password and password != confirm:
            errors.append({'message': 'Your passwords do not match'})
        if not errors:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                resp = {"registered":True, "errors":errors}
                return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
            except Exception as ex:
                errors.append({'message': str(ex)})
                resp = {"registered":False, "errors":errors}
                return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
        else:
            resp = {"login":False, "errors":errors}
            return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
    return render_to_response("register.html", {'errors': errors}, RequestContext(request))
