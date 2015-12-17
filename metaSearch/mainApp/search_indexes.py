import datetime
from haystack import indexes
from mainApp.models import Project

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='title')
#pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
