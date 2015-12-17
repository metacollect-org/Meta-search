from django.http import Http404
from django.shortcuts import render
from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from haystack.forms import SearchForm

from .models import Project

def index(request):

    orga_list = SearchQuerySet().all()[:5]

    #orga_list = Project.objects.order_by('title')[:5]
    context = {'orga_list': orga_list}
    return render(request, 'mainApp/index.html', context)

def detail(request, project_id):
    print("ints")
    try:
        orga = Project.objects.get(pk=project_id)
        print(orga)
    except Project.DoesNotExist:
        raise Http404("Organisation does not exist")
    return render(request, 'mainApp/detail.html', {'orga': orga})

def search_titles(request):
    projects = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))
    return render_to_response('mainApp/ajax_search.html', {'projects':projects})
