from django.shortcuts import render

# Create your views here.
from .security import get_data
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

all_data,resource_query = get_data()
visitor = 0

#print(all_data,resource_query)


def update(request):
    global all_data,resource_query
    #update buffer data and redirect to index page
    all_data,resource_query = get_data()
    #print(all_data,resource_query)
    return HttpResponseRedirect("../")



def index(request):
    global all_data,resource_query,visitor
    # main page
    visitor+=1
    template = loader.get_template('index.html')
    #print(resource_query)
    return HttpResponse(template.render({"all_data":all_data,"resource_query":resource_query["all_item"],"cata_filter":resource_query["all_cata"],"visitor":visitor,"pic_num":len(resource_query["all_item"])}, request))




