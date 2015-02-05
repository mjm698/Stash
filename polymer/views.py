import json
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from datetime import datetime
from polymer.models import *

def home(request):
    return render_to_response('index.html', {}, RequestContext(request))
