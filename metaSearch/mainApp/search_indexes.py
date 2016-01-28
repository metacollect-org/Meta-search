import datetime
from haystack import indexes
from mainApp.models import Project

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    area_city = indexes.CharField()
    categoryName = indexes.CharField()

    content_auto = indexes.EdgeNgramField(model_attr='title')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')
    geo_location = indexes.LocationField(model_attr='get_location')
    geo_location_address = indexes.CharField(model_attr='get_location_address')

    def prepare_categoryName(self, object):
        return [category.name for category in object.categories.all()]

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
