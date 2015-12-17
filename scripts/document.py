from datetime import datetime
from elasticsearch_dsl import Mapping, Field, Index, DocType, String, Date#, Integer
from elasticsearch_dsl.connections import connections
from geopy.geocoders import Nominatim, ArcGIS

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])
geolocator = ArcGIS()

DB_NAME = "db"

class Document(DocType):
    title = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    description = String(analyzer='snowball')
    area = String(analyzer='snowball')
    categories = String(analyzer='snowball')
    languages = String(analyzer='snowball')
    hashtags = String(index='not_analyzed')
    timestamp = Date()
    releasedate = Date()
    entrydate = Date()


    class Meta:
        index = DB_NAME

    def save(self, ** kwargs):
       try:
          loc = geolocator.geocode(self.area)
          tmp = [loc.latitude, loc.longitude]
          self.location = str(loc.latitude)+','+str(loc.longitude)
          self.tmp = tmp
          print tmp
       except Exception as e:
          print e
       return super(Document, self).save(** kwargs)

    def is_online(self):
      if self.releasedate is not None:
         return datetime.now() < self.releasedate
      else: return False

# create the mappings in elasticsearch
Document.init()
m = Mapping('document')
m.field('location', 'geo_point')
m.save(DB_NAME)


db = Index(DB_NAME)
# define custom settings
db.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# create and save a document
#doc = Document(meta={'id': 42}, title='Hello world!', tags=['test'])
#doc.description = ''' looong text '''
#doc.timestamp = datetime.now()
#doc.save()

#doc = Document.get(id=42)
#print(doc.is_online())

# Display cluster health
#print(connections.get_connection().cluster.health())