from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import MyRegistrationForm
from django.http import Http404
from django.utils import translation
from django.shortcuts import render
from django.shortcuts import redirect
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Clean
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
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
    categories = Category.objects.all().filter(parent=None).order_by('name')
    c = Category.getCategoryTree()
    print(c)
    context = {'categories': categories}
    return render(request, 'mainApp/index.html', context)

def data(request):
    return render(request, 'mainApp/data.html')

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
    print(project.url)
    return render(request, 'mainApp/detail.html', {'project': project, 'desc': desc})

def search_fulltext(request):
    search_text = request.GET.get('query')
    print("Search_Text : " + str(search_text))
    if search_text == None or search_text == '' :
        filtered_projects = Project.objects.all()
    else :
        ids = HayStackUtilities.search_fulltext_ids(search_text)
        filtered_projects = Project.objects.all().filter(pk__in=ids)

    category_ids = request.GET.getlist('category')

    print(category_ids)

    for cat_id in category_ids:
        filtered_projects = filtered_projects.filter(categories__id=cat_id)

    # if 'query' in request.GET and request.GET['query'] != '':
    #     project_list = SearchQuerySet().filter(text__startswith=request.GET.get('query',''))
    #     #project_list = SearchQuerySet().autocomplete(content_auto=request.GET.get('query',''))
    #     #project_list = SearchQuerySet().filter(categoryName=AutoQuery(request.GET.get('query')))
    #     project_list = project_list | SearchQuerySet().filter(categoryName__in=request.GET.get('query').split(' '))
    #     #project_list = SearchQuerySetWrapper(project_list)
    # else:
    #     project_list = SearchQuerySet().filter(categoryName__in=request.GET.getlist('category'))
    #     #project_list = Project.objects.filter(categories__in=request.GET.getlist('category'))
    #
    # #project_list = project_list.filter(categories__in=request.GET.getlist('category'))
    # project_list = SearchQuerySetWrapper(project_list)
    for project in filtered_projects:
        print(len(project.categories.all()))
    context = {'project_list': filtered_projects}
    return render(request, 'mainApp/index.html', context)

def search_titles(request):
    print(request.GET.get('q'))
    projects = None
    if request.GET.get('q') and len(request.GET.get('q')) > 3:
        projects = SearchQuerySet().filter(content_auto=request.GET.get('q', ''))
        projects = SearchQuerySetWrapper(projects)
    elif request.GET.getlist('category'):
        projects = Project.objects.all()
    else:
        projects = None

    category_ids = request.GET.getlist('category')

    print(category_ids)

    for cat_id in category_ids:
        projects = projects.filter(categories__id=cat_id)

    return render_to_response('mainApp/ajax_search.html', {'project_list':projects})

def do_logout(request):
    logout(request)
    return redirect('/mainApp')


def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/mainApp')

def register(request):
    form = MyRegistrationForm()
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object
        print(form)
        if form.is_valid():
            user = form.save()
            authenticate(username=user.username, password=user.password)
            login(request, user)
            return HttpResponseRedirect('/mainApp/')
    args = {}
    args.update(csrf(request))
    args['form'] = form
    print(args)
    return render(request, 'registration/register.html', args)



class ProjectNewView(generic.edit.CreateView):
    model = Project
    fields = [] # Excluding updated_at and created_at as the property 'auto_now_add=True' makes them read-only, resulting in an error when adding them to this form.
    for f in Project._meta.get_fields():
        if f.name != 'updated_at' and f.name != 'created_at':
            fields.append(f.name)

    template_name = 'mainApp/new.html'

class ProjectDelete(generic.edit.DeleteView):
    model = Project
    success_url = reverse_lazy('index')

class ProjectEdit(generic.edit.UpdateView):
    model = Project
    fields = ['title']
    template_name = 'mainApp/edit.html'

#class ProjectDataView(generic.edit.CreateView):
#    model = Project
#    fields = [] # Excluding updated_at and created_at as the property 'auto_now_add=True' makes them read-only, resulting in an error when adding them to this form.
#    for f in Project._meta.get_fields():
#        if f.name != 'updated_at' and f.name != 'created_at':
#            fields.append(f.name)
#
#    template_name = 'mainApp/data.html'
