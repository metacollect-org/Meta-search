from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldError
from rest_framework import viewsets
from mainApp.serializers import ProjectSerializer, CategorySerializer, KindSerializer, PageLanguageSerializer, ProgrammingLanguageSerializer
from mainApp.models import Project, Category, ProgrammingLanguage, Kind, PageLanguage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from mainApp.haystackUtil import SearchQuerySetWrapper
from haystack.inputs import AutoQuery
from mainApp.customExceptions import FieldWrong
from mainApp.elastic_util import GeoSearch


@api_view(['GET'])
def project_search_fulltext(request, text, format=None):
    resultList = SearchQuerySet().filter(content=AutoQuery(text))
    resultList = SearchQuerySetWrapper(resultList)
    print(resultList.count())
    if resultList.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(resultList, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_project(request, format=None):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(Project.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )

    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(currentResults, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def search_category(request, format=None):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(Category.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )
    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(currentResults, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_kind(request, format=None):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(Kind.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )
    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = KindSerializer(currentResults, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_language(request, format=None):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(PageLanguage.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )
    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PageLanguageSerializer(currentResults, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_radius(request, format=None):
    '''
    Search for projects in a radius around a specific geoloaction.
    '''

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    radius = request.GET.get('rad')
    max_results = request.GET.get('max')

    geo = GeoSearch()
    geo_results = geo.query_distance(lat=lat, lon=lon, size=max_results, dis=radius)

    ids = []
    for (id, distance) in geo_results:
        ids.append(id)

    project_results = Project.objects.filter(id__in=ids)

    serializer = ProjectSerializer(project_results, many=True)
    return Response(serializer.data)



def apply_filters(all_objects, params):
    '''
    Applies the filters passed as Params to the QuerySet all_objects

    The Params shall be a list of 3-tuples. Each tuple contains a field, an action
    and a value in the form of (field, action, value). This will be passed to
    the django-method: SearchQuerySet.filter(field__action: value)
    '''
    for (key,action, values) in params:
        search_field = key + '__' + action if action != '' else key
        for value in values:
            try:
                all_objects = all_objects.filter(**{search_field: value})
            except FieldError:
                raise FieldWrong(search_field, value)
    return all_objects

def deconstruct_params(params):
    '''
    Takes the request object and extracts the database-queries from the get-params.

    Each parameter of the get-request has to be in the format "foo*bar=value".
    This function converts these get-params to a list of 3-tuples in the format:
    [(foo1, bar1, value1), (foo2, bar2, value2)...]. The Parameter "format=xxx" and
    "page=xxx" are ignored.
    '''
    params_list = []
    params_raw = params.GET.lists()
    for (key, value) in params_raw:
        if key == 'format' or key == 'page':
            continue
        field_action_list = key.split('*')
        if len(field_action_list) > 2 :
            raise Exception('underscoretm','Too Many Underscores')
        params_list.append((field_action_list[0], field_action_list[1] if len(field_action_list) > 1 else '', value))
    return params_list