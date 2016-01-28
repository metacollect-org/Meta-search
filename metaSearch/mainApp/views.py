from django.http import Http404
from django.utils import translation
from django.shortcuts import render
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Clean
from django.shortcuts import render_to_response
from django.views import generic
from haystack.forms import SearchForm
from django.core.urlresolvers import reverse
from .haystackUtil import HayStackUtilities
from mainApp.haystackUtil import SearchQuerySetWrapper
from .models import Project
from .models import Category
from .models import PageLanguage
import random

def queryset_gen(search_qs):
    for item in search_qs:
        yield item.objects

def index(request):
    all_results = SearchQuerySetWrapper(SearchQuerySet().all())
    project_list = [all_results[random.randint(0, all_results.count()-1)] for x in range(0,5)]

    categories = Category.objects.all().order_by('name')

    context = {'project_list': project_list, 'categories': categories}
    return render(request, 'mainApp/index.html', context)

def detail(request, project_id):
    print("ints")
    try:
        project = Project.objects.get(pk=project_id)

        try:
            lang_code = PageLanguage.objects.get(abbreviation=translation.get_language()).abbreviation
        except PageLanguage.DoesNotExist:
            lang_code = 'de'
        desc = project.get_description()

    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    return render(request, 'mainApp/detail.html', {'project': project, 'desc': desc})

def search_fulltext(request):
    if 'query' in request.GET and request.GET['query'] != '':
        project_list = SearchQuerySet().filter(text__startswith=request.GET.get('query',''))
        #project_list = SearchQuerySet().autocomplete(content_auto=request.GET.get('query',''))
        #project_list = SearchQuerySet().filter(categoryName=AutoQuery(request.GET.get('query')))
        project_list = project_list | SearchQuerySet().filter(categoryName__in=request.GET.get('query').split(' '))
        #project_list = SearchQuerySetWrapper(project_list)
    else:
        project_list = SearchQuerySet().filter(categoryName__in=request.GET.getlist('category'))
        #project_list = Project.objects.filter(categories__in=request.GET.getlist('category'))

    #project_list = project_list.filter(categories__in=request.GET.getlist('category'))
    project_list = SearchQuerySetWrapper(project_list)
    context = {'project_list': project_list}
    return render(request, 'mainApp/index.html', context)

def search_titles(request):
    print(request.GET.get('q'))
    projects = None
    if len(request.GET.get('q')) > 3:
        projects = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
        projects = SearchQuerySetWrapper(projects)

    return render_to_response('mainApp/ajax_search.html', {'projects':projects})


class ProjectNewView(generic.edit.CreateView):
    model = Project
    fields = [] # Excluding updated_at and created_at as the property 'auto_now_add=True' makes them read-only, resulting in an error when adding them to this form.
    for f in Project._meta.get_fields():
        if f.name != 'updated_at' and f.name != 'created_at':
            fields.append(f.name)

    #fields = [f.name for f in Project._meta.get_fields()]
    template_name = 'mainApp/new.html'
