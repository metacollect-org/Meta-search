from django.http import Http404
from django.shortcuts import render

from .models import Project

def index(request):
    orga_list = Project.objects.order_by('title')[:5]
    context = {'orga_list': orga_list}
    return render(request, 'mainApp/index.html', context)

def detail(request, project_id):
    try:
        orga = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Organisation does not exist")
    return render(request, 'mainApp/detail.html', {'orga': orga})
