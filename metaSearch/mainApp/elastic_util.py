__author__ = 'jens'

from elasticsearch import Elasticsearch
from metaSearch.settings import HAYSTACK_CONNECTIONS
#import numpy as np
import math as np
from operator import itemgetter

DEFAULT_GEO_LOC = (51.0834196, 10.4234469, 'Germany')  # Center of Germany
MODEL_TYPE = 'modelresult'
AREA_LOCATION = 'location'
CONTACT_LOCATION = 'contact_location'


def convert(hit, location_field, query_point):
    id = hit['django_id']
    location_point = hit[location_field].split(',')
    dis = distance(location_point, query_point)
    return id, dis  #, hit['content_auto']


def distance(p1, p2):
    p1lat, p1lon = float(p1[0]), float(p1[1])
    p2lat, p2lon = float(p2[0]), float(p2[1])
    latdiff = (p2lat + p1lat) / 2 * 0.01745
    dlat = 111.3 * np.fabs(p1lat - p2lat)
    dlon = 111.3 * np.cos(latdiff) * np.fabs(p1lon - p2lon)
    return np.sqrt(np.pow(dlat, 2) + np.pow(dlon, 2))


class GeoSearch():
    es = Elasticsearch()
    index = HAYSTACK_CONNECTIONS['default']['INDEX_NAME']


    def query_distance(self, lat=DEFAULT_GEO_LOC[0], lon=DEFAULT_GEO_LOC[1], dis='500km', _type=MODEL_TYPE,
                       field=AREA_LOCATION, size=999):
        response = self.es.search(index=self.index, size=size,
                                  body={
                                      "query": {
                                          "match_all": {}
                                      },
                                      "filter": {
                                          "geo_distance": {
                                              "distance": dis,
                                              _type + '.' + field: {
                                                  "lat": lat,
                                                  "lon": lon
                                              }
                                          }
                                      }
                                  })
        result = [convert(hit['_source'], field, (lat, lon)) for hit in response['hits']['hits']]
        return sorted(result, key=itemgetter(1))

    def query_address(self, address, dis, _type=MODEL_TYPE, field=AREA_LOCATION, size=999):
        pass

# USAGE:
# geo = GeoSearch()
# for result in geo.query_distance():
#     print(result)