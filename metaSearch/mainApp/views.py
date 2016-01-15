from django.http import Http404
from django.shortcuts import render
from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from django.views import generic
from haystack.forms import SearchForm
from django.core.urlresolvers import reverse

from .models import Project

def index(request):
    project_list = SearchQuerySet().all()[:5]

    #orga_list = Project.objects.order_by('title')[:5]
    context = {'project_list': project_list}
    return render(request, 'mainApp/index.html', context)

def detail(request, project_id):
    print("ints")
    try:
        project = Project.objects.get(pk=project_id)
        print(project)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    return render(request, 'mainApp/detail.html', {'project': project})

def search_titles(request):
    projects = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))
    return render_to_response('mainApp/ajax_search.html', {'projects':projects})


class ProjectNewView(generic.edit.CreateView):
    model = Project
    fields = [f.name for f in Project._meta.get_fields()]
    #fields = ['title', 'languages']
    template_name = 'mainApp/new.html'
