from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from mainApp.serializers import ProjectSerializer, CategorySerializer, KindSerializer, PageLanguageSerializer, ProgrammingLanguageSerializer
from mainApp.models import Project, Category, ProgrammingLanguage, Kind, PageLanguage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from mainApp.haystackUtil import HayStackUtilities
from haystack.inputs import AutoQuery



@api_view(['GET'])
def project_list(request):
    """
    List all Projects, or create a new snippet.
    """
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def project_detail(request, pk):
    """
    Retrieve, update or delete a project instance.
    """
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("IN THING")
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
@api_view(['GET'])
def project_search_fulltext(request, text):
    print(text)
    wrappedpro = SearchQuerySet().filter(content=AutoQuery(text))
    resultList = HayStackUtilities.unwrapResult(wrappedpro)
    print(resultList)
    if len(wrappedpro) == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(resultList, many=True)
    return Response(serializer.data)



#
# class ProjectViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Project.objects.all().order_by('-created_at')
#     serializer_class = ProjectSerializer
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
# class KindViewSet(viewsets.ModelViewSet):
#     queryset = Kind.objects.all()
#     serializer_class = KindSerializer
#
# class PageLanguageViewSet(viewsets.ModelViewSet):
#     queryset = PageLanguage.objects.all()
#     serializer_class = PageLanguageSerializer
#
# class ProgrammingLanguageViewSet(viewsets.ModelViewSet):
#     queryset = ProgrammingLanguage.objects.all()
#     serializer_class = ProgrammingLanguageSerializer
#

