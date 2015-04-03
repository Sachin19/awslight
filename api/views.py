from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt 

from utility import Utility
import helppages

# Create your views here.
def index(request):
	# print 'we are here'
	basicResponse = helppages.basicGuideLine()
	return HttpResponse(basicResponse)

@csrf_exempt
def basicsummarize(request):
	if 'Text' in request.POST and len(request.POST['Text'])>0:
		text = request.POST['Text']
		summary = Utility.summarize(text)
		return HttpResponse(summary)
	else:
		# return HttpResponse("Error")
		return HttpResponse(helppages.basicGuideLine())