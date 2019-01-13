from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('smartmeter/index.html')
    context = {
        'test': 'test',
    }
    return HttpResponse(template.render(context, request))
