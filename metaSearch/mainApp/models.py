from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

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
class PageLanguage(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)
    alternatives = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True)
    def __str__(self):
        return self.name

# Create your models here.
class GeoLocation(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    def __str__(self):
        return str([self.lat, self.lon])

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
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
    geo_location = models.ManyToManyField(GeoLocation, blank=True)
    status = models.IntegerField(choices=STATUS)
    logo = models.URLField(null=True, blank=True, default=default_logo)
    contact_socialmedia_fb = models.URLField(null=True, blank=True)
    contact_socialmedia_twitter = models.URLField(null=True, blank=True)
#    contact_socialmedia = models.URLField(null=True, blank=True) # comma separated
    contact_telephone = models.CharField(max_length=200, blank=True, default='') # comma separated
    contact_address_street = models.CharField(max_length=200, blank=True, default='')
    contact_address_housenr = models.CharField(max_length=20, blank=True, default='')
    contact_address_zip = models.CharField(max_length=20, blank=True, default='')
    contact_address_city = models.CharField(max_length=200, blank=True, default='')
    contact_address_country = models.CharField(max_length=200, blank=True, default='')
    languages = models.ManyToManyField(PageLanguage) # multiple
    needs = models.CharField(max_length=200, blank=True, default='') # optional
    programming_languages = models.ManyToManyField(ProgrammingLanguage, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def has_full_contact(self):
        return (self.contact_address_housenr != '' and self.contact_address_street != '' and (self.contact_address_city != '' or self.contact_address_zip != ''))

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

    def is_online(self):
        return self.status==1
