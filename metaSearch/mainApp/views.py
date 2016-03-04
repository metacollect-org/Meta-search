from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.utils import translation
from django.shortcuts import render, redirect, render_to_response
from haystack.inputs import AutoQuery, Clean
from haystack.query import SearchQuerySet

from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator

from mainApp.models import init_geo_locations

import ast

from .forms import MyRegistrationForm, UpdateProfile
from .JoinForm import JoinForm
from .haystackUtil import HayStackUtilities, SearchQuerySetWrapper
from .models import Category
from .models import PageLanguage
from .models import Project


def queryset_gen(search_qs):
    for item in search_qs:
        yield item.objects

def index(request):
    categories = Category.objects.all().filter(parent=None).order_by('name')
    # c = Category.getCategoryTree()
    # print(c)
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
    categories = Category.objects.all().filter(parent=None).order_by('name')
    # c = Category.getCategoryTree()
    # print(c)
    context = {'project_list': filtered_projects, 'query': search_text, 'categories': categories}
    return render(request, 'mainApp/search_results.html', context)



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

@login_required
def user_profile(request):
    args = {}
    print(request.user.email)
    data = {'username': request.user.username, 'email': request.user.email}
    form = UpdateProfile(request.POST, instance=request.user)
    form.base_fields['username'].initial = request.user.username
    form.base_fields['email'].initial = request.user.email
    if request.method == 'POST':
        # form = UpdateProfile(request.POST, )
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse('update_profile_success'))
    else:
        form = UpdateProfile()

    args['form'] = form
    return render(request, 'mainApp/userProfile.html', args)

@login_required
def user_projects(request):
    print(request.user.pk)
    project_list = get_objects_for_user(request.user, 'change_project', klass=Project)

    context = {'projects': project_list}
    return render(request, 'mainApp/userProjects.html', context)

@login_required
def join_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JoinForm(request.POST)
        formcopy = JoinForm(request.POST.copy())
        # populate data for model init
        # manipulate post request (form.data)
        category_ids = []
        for field in request.POST:
            if type(field) is str:
                if field.startswith('category'):
                    category_ids += [request.POST[field]]

        if len(category_ids) > 0:
            formcopy.data.setlist('categories', category_ids)
        form = JoinForm(formcopy.data)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            obj = form.save(commit=True)
            #init_geo_locations(instance=obj)
            obj.created_by = request.user
            obj.save()

            assign_perm('change_project', request.user, obj) # give user permission to change the project
            assign_perm('change_project', Group.objects.get(name='editors'), obj) # give editors permission to change project
            # redirect to a new URL:
            return detail(request, obj.id)
        else:
            print(form.errors.as_json())
    # if a GET (or any other method) we'll create a blank form
    else:
        form = JoinForm()

    return render(request, 'mainApp/new.html', {'form': form})

@login_required
def delete_page(request, project_id):
    return render(request, 'registration/not_allowed_delete.html')



@login_required
def edit_page(request, project_id):

    selected_project = Project.objects.get(pk=project_id)
    print(request.user.has_perm('change_project', selected_project))

    if not request.user.has_perm('change_project', selected_project):
        return render(request, 'registration/not_allowed_edit.html')

    print(selected_project.pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JoinForm(request.POST)
        formcopy = JoinForm(request.POST.copy())
        # populate data for model init
        # manipulate post request (form.data)
        category_ids = []
        for field in request.POST:
            if type(field) is str:
                if field.startswith('category'):
                    category_ids += [request.POST[field]]

        print(category_ids)
        if len(category_ids) > 0:
            formcopy.data.setlist('categories', category_ids)
        form = JoinForm(formcopy.data, instance=selected_project)

        print(form.is_valid())
        print(form.instance.id)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            obj = form.save(commit=True)

            # for id in category_ids:
            #     obj.categories.add(Category.objects.get(pk=id))
            #init_geo_locations(instance=obj)
            #obj.save()
            # redirect to a new URL:
            return detail(request, obj.id)
        else:
            print(form.errors.as_json())
    # if a GET (or any other method) we'll create a blank form
    else:
        print('GET')
        form = JoinForm(instance=selected_project)

    return render(request, 'mainApp/edit.html', {'form': form})
