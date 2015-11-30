from django.http import Http404
from django.shortcuts import render

from .models import Organisation

def index(request):
    orga_list = Organisation.objects.order_by('title')[:5]
    context = {'orga_list': orga_list}
    return render(request, 'mainApp/index.html', context)

def detail(request, organisation_id):
    try:
        orga = Organisation.objects.get(pk=organisation_id)
    except Organisation.DoesNotExist:
        raise Http404("Organisation does not exist")
    return render(request, 'mainApp/detail.html', {'orga': orga})
