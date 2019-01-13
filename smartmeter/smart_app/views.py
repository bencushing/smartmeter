from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt, mpld3

# Create your views here.
def index(request):
    template = loader.get_template('smart_app/index.html')
    context = {
        'test': 'test',
    }
    return HttpResponse(template.render(context, request))

	
def graph(request):
     fig = plt.figure()
     plt.plot([1,2,3,4])
     g = mpld3.fig_to_html(fig)
     return HttpResponse(g)