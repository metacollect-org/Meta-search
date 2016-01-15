from django.http import Http404
from django.shortcuts import render
from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from django.views import generic
from haystack.forms import SearchForm
from django.core.urlresolvers import reverse

from .models import Project
from .models import Category
from .models import PageLanguage

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
    fields = '__all__'
    template_name = 'mainApp/new.html'
    
    def get(self, request):
        selectCategories = Category.objects.all()
        pageLanguages = PageLanguage.objects.all()
        fields = [f.name for f in Project._meta.get_fields()]
        return render(request, 'mainApp/new.html', {'selectCategories': selectCategories, 'pageLanguages': pageLanguages, 'fields': fields,}) 

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         title = request.POST.get('title')
    #         url = request.POST.get('url')
    #         kind = request.POST.get('kind')
    #         organisation_name = request.POST.get('organisation_name')
    #         description = request.POST.get('description')
    #         area_country = request.POST.get('area_country')
    #         area_state = request.POST.get('area_state')
    #         area_city = request.POST.get('area_city')
    #         status = request.POST.get('status')
    #         logo = request.POST.get('logo')
    #         contact_socialmedia = request.POST.get('contact_socialmedia')
    #         contact_telephone = request.POST.get('contact_telephone')
    #         contact_address_street = request.POST.get('contact_address_street')
    #         contact_address_housenr = request.POST.get('contact_address_housenr')
    #         contact_address_zip = request.POST.get('contact_address_zip')
    #         contact_address_city = request.POST.get('contact_address_city')
    #         contact_address_country = request.POST.get('contact_address_country')
    #         needs = request.POST.get('needs')
    #         categories = request.POST.get('categories')
    #         languages = request.POST.get('languages')
    #         programming_languages = request.POST.get('programming_languages')
    #         obj = Project.objects.create(title = title, url = url, kind = kind, organisation_name = organisation_name, description = description, area_country = area_country, area_state = area_state, area_city = area_city, status = status, logo = logo, contact_socialmedia = contact_socialmedia, contact_telephone = contact_telephone, contact_address_street = contact_address_street, contact_address_housenr = contact_address_housenr, contact_address_zip = contact_address_zip, contact_address_city = contact_address_city, contact_address_country = contact_address_country, needs = needs, categories = categories, languages = languages, programming_languages = programming_languages)
    #         obj.save(force_insert=True)
    #         return HttpResponse('This is POST request')
