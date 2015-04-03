from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.
def index(request):
	# print 'we are here'
	return HttpResponse("You have reached the home page of Summarizer API. Please use POST or GET request to do stuff")

@csrf_exempt
def basicsummarize(request):
	return HttpResponse("You called basic summarize function")	