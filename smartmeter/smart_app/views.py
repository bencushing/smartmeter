from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('smart_app/index.html')
    context = {
        'test': 'test',
    }
    return HttpResponse(template.render(context, request))
