from django.db import models
from django.conf import settings

STATUS = (
    (0, 'Inactive'),
    (1, 'Active'),
    (2, 'In Progress'),
    (3, 'Unspecified'),
)

KINDS = (
    (0, 'Website'),
    (1, 'App'),
    (2, 'Map'),
    (3, 'Facebook'),
    (4, 'Unspecified'),
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

class PageLanguage(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)
    alternatives = models.CharField(max_length=200)

    def __str__(self):
        return self.name;

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True)
    def __str__(self):
        return self.name

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    kind = models.IntegerField(choices=KINDS) # multiple
    organisation_name = models.CharField(max_length=200, blank=True, default='')
    categories = models.ManyToManyField(Category)

    description_de = models.TextField()
    description_en = models.TextField(blank = True, default='')

    area_country = models.CharField(max_length=200, blank=True, default='')
    area_state = models.CharField(max_length=200, blank=True, default='') # bundesland
    area_city = models.CharField(max_length=200, blank=True, default='')
    status = models.IntegerField(choices=STATUS)
    logo = models.URLField(null=True, blank=True, default=default_logo)
    contact_socialmedia = models.URLField(null=True, blank=True) # comma separated
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

    def get_description(self, lang_code):
        if not getattr(self, 'description_'+lang_code):
            return getattr(self, 'description_de')
        return getattr(self, 'description_'+lang_code)

    def is_online(self):
        return self.status==1
