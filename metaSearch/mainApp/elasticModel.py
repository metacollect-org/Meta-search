import string
import random

from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Nested, Boolean, analyzer, Integer

def random_string(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class Project(DocType):
    title = String()
    url = String()
    kind = Integer()
    organisation_name = String()
    categories = Integer()
    description_en = String()
    area_country = String()
    area_city = String()
    area_state = String()
    status = Integer()
    logo = String()
    contact_socialmedia = String()
    contact_telephone = String()
    contact_address_street = String()
    contact_address_zip = String()
    contact_address_housenr = String()
    contact_address_city = String()
    contact_address_country = String()
    languages = Integer()
    needs = String()
    programming_language = Integer()
    created_at = Date()

    class Meta:
        index = 'projects'

    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super().save(** kwargs)

    def random_int(max=20):
        return random.randint(0,max)


    def random_project(self):
        self.title = self.random_string()
        self.url = self.random_string().join('.com')
        self.kind = self.random_int(3)
        self.organisation_name = self.random_string().join(' e.v.')
        self.categories = self.random_int(4)
        self.description_en = self.random_string()
        self.area_country = self.random_string()
        self.area_state = self.random_string()
        self.area_city = self.random_string()
        self.status = self.random_int(3)
        self.logo = self.random_string()
        self.contact_socialmedia = self.random_string()
        self.contact_telephone = self.random_string()
        self.contact_address_street = self.random_string().join(' Straße')
        self.contact_address_zip = self.random_string()
        self.contact_address_housenr = self.random_int(100)
        self.contact_address_city = self.area_city
        self.contact_address_country = self.area_country
        self.languages = self.random_int(5)
        self.needs = self.random_string()
        self.programming_language = self.random_int(2)


