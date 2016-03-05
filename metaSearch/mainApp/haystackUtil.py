from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Clean
from mainApp.models import Project

class SearchQuerySetWrapper(object):
    """
    Decorates a SearchQuerySet object using a generator for efficient iteration
    found at http://stackoverflow.com/questions/13642617/django-haystack-searchqueryset-to-queryset
    """
    def __init__(self, qs):
        self.qs = qs

    def count(self):
        return self.qs.count()

    def __iter__(self):
        for result in self.qs:
            yield result.object

    def __getitem__( self, key):
        if isinstance(key, int) and (key >= 0 or key < self.count()):
            # return the object at the specified position
            return self.qs[key].object
        # Pass the slice/range on to the delegate
        return SearchQuerySetWrapper(self.qs[key])

class HayStackUtilities:

    def unwrapResult(results_list):
        unwrapped_list = []
        for result in results_list:
            unwrapped_list.append(result.object)
        return unwrapped_list

    def search_fulltext_ids(text):
        """
        do a fulltextsearch with Haystack and return only the ids for further
        use with the regular database
        """

        results1 = SearchQuerySet().filter(content=AutoQuery(text))
        results2 = Project.objects.filter(title__contains=text)
        ids = []
        for result in results1:
            ids.append(result.object.id)
        for result in results2:
            ids.append(result.id)
        return ids

    def search_autocomplete_ids(text):
        results = SearchQuerySet().filter(content_auto=text)
        ids=[]
        for result in results:
            ids.append(result.object.id)
        return ids