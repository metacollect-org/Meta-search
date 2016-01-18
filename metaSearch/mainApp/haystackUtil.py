from haystack.query import SearchQuerySet

class HayStackUtilities:

    def unwrapResult(results_list):
        unwrapped_list = []
        for result in results_list:
            unwrapped_list.append(result.object)
        return unwrapped_list