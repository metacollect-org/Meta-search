from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from geopy.geocoders import Nominatim
from django.core.urlresolvers import reverse

import time

WAIT_TIME_GEO_REQUESTS = 2  # in seconds, ABSOLUTE MIN IS 1 SECOND
LOAD_GEO_LOCATIONS = True
DEFAULT_GEO_LOC = (51.0834196, 10.4234469, 'Germany')  # Center of Germany

STATUS = (
    (0, 'Inactive'),
    (1, 'Active'),
    (2, 'In Progress'),
    (3, 'Unspecified'),
)

KINDS = (
    'website',
    'app',
    'map',
    'facebook',
    'offline',
    'unspecified',
)

# Supported languages in the format: ('english name', 'abbreviation', 'alternative names with comma separated')
LANGUAGES_SUPPORTED = (
    ('english', 'en', 'englisch'),
    ('german', 'de', 'deutsch'),
    ('polish', 'pl', 'polnisch, język polski, polszczyzna'),
    ('albanien', 'sq', 'shqip, albanisch'),
    ('romanian', 'ro', 'română, rumänisch'),
    ('bulgarian', 'bg', 'български език, bulgarisch'),
    ('hungarian', 'hu', 'magyar, ungarisch'),
    ('turkish', 'tr', 'türkçe, türkisch'),
    ('serbian', 'sr', 'српски, srpski, serbisch'),
    ('italian', 'it', 'italiano, lingua italiana, italienisch'),
    ('russian', 'ru', 'ру́сский язы́к, russkiy yazyk, russisch'),
    ('syriac', 'syc', 'ܠܫܢܐ ܣܘܪܝܝܐ, Leššānā Suryāyā, syrisch'),
    ('arabic', 'ar', 'العَرَبِية‎, al-ʻarabiyyah, عربى‎, عربي, ʻarabī, arabisch'),
    ('tigrinya', 'ti', 'tigrigna, ትግርኛ, tigriññā, tigrinisch'),
    ('tigre', 'tig', 'ትግረ, tigrē, tigrayit, xasa, الخاصية‎, ḫāṣiyah, ትግሬ, ኻሳ'),
    ('french', 'fr', 'le français, français, la langue française, französisch'),
    ('macedonian', 'mk', 'македонски, македонски јазик, makedonski jazik, mazedonisch'),
    ('persian', 'fa', 'farsi, فارسی, fārsi, persisch'),
    ('urdu', 'ur', 'اُردُو‎, urdū, زبان اردو معلہ‎, zabān-i urdū-yi muʿalla, Sprache des gebildeten Hofes'),
    ('spanish', 'es', 'español, castilian, castellano, spanisch'),
    ('unknown', 'xxx', ''),
)

# English,
# German,

# Polen,
# Albanian,
# Rumänien
# Bulgarien
# Ungarn
# Türkei
# Serbien
# Italien
# Russland
# Syrien
# Irak
# Eritrea


def default_logo():
    return "https://openclipart.org/image/2400px/svg_to_png/201970/refugees-welcome.png"


class Kind(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PageLanguage(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)
    alternatives = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['abbreviation']


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True)

    name_de = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200)
    description = models.TextField(default="No description available")
    description_de = models.TextField(default="Keine Beschreibung Vorhanden")
    description_fr = models.TextField(default="Aucune description disponible")
    description_ar = models.TextField(default="لا يوجد وصف متاح")




    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# Create your models here.
class GeoLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    lat = models.FloatField()
    lon = models.FloatField()
    def __str__(self):
        return self.name


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=400)
    kind = models.ManyToManyField(Kind)
    organisation_name = models.CharField(max_length=200, blank=True, default='')
    categories = models.ManyToManyField(Category)

    description_de = models.TextField()
    description_en = models.TextField(blank = True, default='')
    description_fr = models.TextField(blank = True, default='')
    description_ar = models.TextField(blank = True, default='')

    area_country = models.CharField(max_length=200, blank=True, default='')
    area_state = models.CharField(max_length=200, blank=True, default='') # bundesland
    area_city = models.CharField(max_length=200, blank=True, default='')
    geo_location = models.ForeignKey(GeoLocation, blank=True, null=True)
    status = models.IntegerField(choices=STATUS)
    logo = models.URLField(null=True, blank=True, default=default_logo, max_length=400)
    contact_socialmedia_fb = models.URLField(null=True, blank=True)
    contact_socialmedia_twitter = models.URLField(null=True, blank=True)
#    contact_socialmedia = models.URLField(null=True, blank=True) # comma separated
    contact_telephone = models.CharField(max_length=200, blank=True, default='') # comma separated
    contact_address_street = models.CharField(max_length=200, blank=True, default='')
    contact_address_housenr = models.CharField(max_length=50, blank=True, default='')
    contact_address_zip = models.CharField(max_length=20, blank=True, default='')
    contact_address_city = models.CharField(max_length=200, blank=True, default='')
    contact_address_country = models.CharField(max_length=200, blank=True, default='')
    contact_loc = models.ForeignKey(GeoLocation, blank=True, null=True, related_name='contact_location')
    languages = models.ManyToManyField(PageLanguage) # multiple
    needs = models.CharField(max_length=200, blank=True, default='') # optional
    programming_languages = models.ManyToManyField(ProgrammingLanguage, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def has_full_contact(self):
        return self.contact_address_housenr != '' \
            and self.contact_address_street != '' \
            and (self.contact_address_city != '' or self.contact_address_zip != '')

    def get_description(self):
        lang_code = translation.get_language()
        if not getattr(self, 'description_'+lang_code):
            if getattr(self, 'description_de'):
                return getattr(self, 'description_de')
            elif getattr(self, 'description_en'):
                return getattr(self, 'description_en')
            else:
                return _('No description available')
        return getattr(self, 'description_'+lang_code)

    def get_page_languages(self):
        if not self.languages.all():
            return _('Translations are not known')
        output = ''
        for lang in self.languages.all():
            output += lang.name + '; '
        return output

    def get_categories(self):
        if not self.categories.all():
            return _('Belongs to no categories')
        output = ''
        for cat in self.categories.all():
            output += cat.name + '; '
        return output

    def get_languages(self):
        if self.languages is None:
            return 'unknown'
        out = ''
        for lang in self.languages.all():
            out += lang.name + ', '
        if out == '':
            return 'unknown'
        return out

    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_id': self.pk})

    def get_location(self):
        if not hasattr(self, 'geo_location') or \
            self.geo_location is None:
                return "%s,%s" % (DEFAULT_GEO_LOC[0], DEFAULT_GEO_LOC[1])
        return "%s,%s" % (self.geo_location.lat, self.geo_location.lon)

    def get_contact_loc(self):
        if not hasattr(self, 'contact_location') or \
            self.contact_location is None:
                return "%s,%s" % (DEFAULT_GEO_LOC[0], DEFAULT_GEO_LOC[1])
        return "%s,%s" % (self.contact_location.lat, self.contact_location.lon)

    def get_location_address(self):
        if not hasattr(self, 'geo_location') or \
            self.geo_location is None:
                return DEFAULT_GEO_LOC[2]
        return self.geo_location.address

    def get_contact_address(self):
        if not hasattr(self, 'contact_location') or \
            self.contact_location is None:
                return DEFAULT_GEO_LOC[2]
        return self.contact_location.address

    def get_status_string(self):
        if self.status is None:
            return STATUS[3]
        return STATUS[self.status][1]

    def is_online(self):
        return self.status == 1


geo_locator = Nominatim()


def get_geo_location(location_name):
    if location_name is None:
        return DEFAULT_GEO_LOC[0], DEFAULT_GEO_LOC[1], DEFAULT_GEO_LOC[2]
    if len(location_name) == 0:
        return DEFAULT_GEO_LOC[0], DEFAULT_GEO_LOC[1], DEFAULT_GEO_LOC[2]
    time.sleep(WAIT_TIME_GEO_REQUESTS)
    location = geo_locator.geocode(location_name)
    if location is None:
        return DEFAULT_GEO_LOC[0], DEFAULT_GEO_LOC[1], DEFAULT_GEO_LOC[2]
    print('new location found: '+location.address+' ('+location_name+')')
    return location.latitude, location.longitude, location.address


def init_geo_locations(**kwargs):
    instance = kwargs.get('instance')
    if LOAD_GEO_LOCATIONS:
        for area in [instance.area_city, instance.area_country, instance.area_state, DEFAULT_GEO_LOC[2]]:
            if area is None:
                continue
            if len(area) == 0:
                continue
            try:
                instance.geo_location = GeoLocation.objects.get(name=area)
            except ObjectDoesNotExist:
                lat, lon, address = get_geo_location(area)
                new_location = GeoLocation(lat=lat, lon=lon, address=address, name=area)
                new_location.save()
                instance.geo_location = new_location
            break
        try:
            contact_loc = instance.contact_address_street + ' ' \
                + instance.contact_address_housenr + ', ' \
                + instance.contact_address_zip + ' ' \
                + instance.contact_address_city + ' ' \
                + instance.contact_address_country
            contact_loc = contact_loc.strip(', ')
            if contact_loc != '':
                try:
                    instance.contact_location = GeoLocation.objects.get(name=contact_loc)
                except ObjectDoesNotExist:
                    lat, lon, address = get_geo_location(contact_loc)
                    new_location = GeoLocation(lat=lat, lon=lon, address=address, name=contact_loc)
                    new_location.save()
                    instance.contact_location = new_location
        except Exception as e:
            pass

pre_save.connect(init_geo_locations, Project)
