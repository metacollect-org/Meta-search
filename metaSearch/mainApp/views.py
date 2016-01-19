from django.http import Http404
from django.utils import translation
from django.shortcuts import render
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from django.shortcuts import render_to_response
from django.views import generic
from haystack.forms import SearchForm
from django.core.urlresolvers import reverse
from .haystackUtil import HayStackUtilities
from .models import Project
from .models import Category
from .models import PageLanguage
import random

def index(request):
    all_results = SearchQuerySet().all()
    project_list = [all_results[random.randint(0, all_results.count()-1)] for x in range(0,5)]
    context = {'project_list': HayStackUtilities.unwrapResult(project_list)}
    return render(request, 'mainApp/index.html', context)

def detail(request, project_id):
    print("ints")
    try:
        project = Project.objects.get(pk=project_id)

        try:
            lang_code = PageLanguage.objects.get(abbreviation=translation.get_language()).abbreviation
        except PageLanguage.DoesNotExist:
            lang_code = 'de'
        desc = project.get_description(lang_code)

        print(project)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    return render(request, 'mainApp/detail.html', {'project': project, 'desc': desc})

def search_fulltext(request):
    print("HALLOO")
    print(request.GET)
    project_list = SearchQuerySet().filter(content=AutoQuery(request.GET.get('query','')))
    context = {'project_list': HayStackUtilities.unwrapResult(project_list)}
    return render(request, 'mainApp/index.html', context)


def search_titles(request):
    print(request.GET.get('q'))
    projects = None
    if len(request.GET.get('q')) > 3:
        projects = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
        projects = HayStackUtilities.unwrapResult(projects)

    return render_to_response('mainApp/ajax_search.html', {'projects':projects})


class ProjectNewView(generic.edit.CreateView):
    model = Project
    fields = [] # Excluding updated_at and created_at as the property 'auto_now_add=True' makes them read-only, resulting in an error when adding them to this form.
    for f in Project._meta.get_fields():
        if f.name != 'updated_at' and f.name != 'created_at':
            fields.append(f.name)

    #fields = [f.name for f in Project._meta.get_fields()]
    template_name = 'mainApp/new.html'
