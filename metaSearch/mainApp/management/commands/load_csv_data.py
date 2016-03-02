from django.core.management.base import BaseCommand
import requests
import csv
from mainApp import models
from mainApp.models import Project, Category, ProgrammingLanguage, PageLanguage, Kind, GeoLocation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm


# 0  id
# 1  url +
# 2  title +
# 3  edited_by/finished
# 4  organisation_name
# 5  kind
# 6  CMS
# 7  framework
# 8  responsive
# 9  mobile
# 10 mapping
# 11 status
# 12 organization_type
# 13 area_city
# 14 area_bundesland
# 15 area_country
# 16 description_en
# 17 description_de
# 18 description_fr
# 19 description_ar
# 20 logo
# 21 hashtags
# 22 categories
# 23 orgacontact_name
# 24 orgacontact_email
# 25 orgacontact_language
# 26 contact_email
# 27 contact_phone
# 28 contact_socialmedia_fb
# 29 contact_socialmedia_twitter
# 30 contact_adress_street
# 31 contact_adress_housenr
# 32 contact_adress_postalcode
# 33 contact_adress_city
# 34 contact_adress_state
# 35 contact_adress_country
# 36 code_repository
# 37 programming_languages
# 38 languages
# 39 code_license
# 40 releasedate
# 41 last_update_of_table
# 42 software_development_needs
# 43 random_generated_key
# 44 Flyer




class Command(BaseCommand):
    args = 'No additional Arguments needed'
    help = 'Load the Refugee Project data from the Spreadsheet and put them in the Database'

    def init_page_languages(self) :
        for (name, abb, alternatives) in models.LANGUAGES_SUPPORTED:

            try:
                pl = PageLanguage.objects.get(name=name)
                print('language ' + name + ' already exists.')
            except ObjectDoesNotExist:
                print('adding ' + str(name) + ' ...')
                pl = PageLanguage(name=name, abbreviation=abb, alternatives=alternatives)
                pl.save()
        return

    def init_kinds(self) :

        for kind in models.KINDS:
            selKind = Kind.objects.filter(name=kind.strip().lower())
            if len(selKind) == 0:
                k = Kind(name=kind.strip().lower())
                k.save()
        return

    def init_categories(self):
        csvReader = csv.reader(getCategoriesCsvData().split('\n'), delimiter=',')
        first_line= csvReader.__next__() # skip the first row, because these are the column names
        second_line = csvReader.__next__()
        print(first_line)
        print(second_line)

        for row in csvReader:
            category_en = row[1]
            subcat_en = row[2]
            description_en = row[3]
            category_de = row[4]
            subcat_de = row[5]
            description_de = row[6]
            category_fr = row[7]
            subcat_fr = row[8]
            description_fr = row[9]
            category_ar = row[10]
            subcat_ar = row[11]
            description_ar = row[12]
            if category_en.strip() == '': continue

            print(category_en, subcat_en)

            if subcat_en.strip() == "":
                dbcat, created = Category.objects.get_or_create(name=category_en, parent=None)
                print(created)
                # cats = Category.objects.all().filter(name=category_en)
                # exists = False
                # if len(cats) != 0:
                #     for cat in cats:
                #         if cat.parent == None:
                #             exists = True
                #             break
                # if exists: continue
                # dbcat = Category(name=category_en)
                dbcat.description = description_en if description_en.strip() != "" else dbcat.description
                dbcat.name_de = category_de
                dbcat.description_de = description_de if description_de.strip() != "" else dbcat.description_de
                dbcat.name_fr = category_fr
                dbcat.description_fr = description_fr if description_fr.strip() != "" else dbcat.description_fr
                dbcat.name_ar = category_ar
                dbcat.description_ar = description_ar if description_ar.strip() != "" else dbcat.description_ar
                dbcat.save()
            else:
                if Category.objects.filter(name=subcat_en, parent__name=category_en).count() == 0:
                    newSubCat = Category(name=subcat_en)
                else:
                    newSubCat = Category.objects.get(name=subcat_en, parent__name=category_en)
                newSubCat.description = description_en if description_en.strip() != "" else newSubCat.description
                newSubCat.name_de = subcat_de
                newSubCat.description_de = description_de if description_de.strip() != "" else newSubCat.description_de
                newSubCat.name_fr = subcat_fr
                newSubCat.description_fr = description_fr if description_fr.strip() != "" else newSubCat.description_fr
                newSubCat.name_ar = subcat_ar
                newSubCat.description_ar = description_ar if description_ar.strip() != "" else newSubCat.description_ar
                parCat = Category.objects.get(name=category_en, parent=None)
                newSubCat.parent=parCat
                newSubCat.save()




    def handle(self, *args, **options):
        self.stdout.write("Initializing Languages...")
        self.init_page_languages()
        print("Initializing Kinds")
        self.init_kinds()
        print("Initializing Categories")
        self.init_categories()
        print("Initializing Projects")

        #group of users, which are allowed to edit each project
        editors, created = Group.objects.get_or_create(name='editors')
        if created:
            editors.save()

        csvReader = csv.reader(getProjectCsvData().split('\n'), delimiter=',')
        first_line= csvReader.__next__() # skip the first row, because these are the column names
        print(first_line)
        project_count = 0
        for row in csvReader:
            if row[2].strip() != '': # only take the ones, that have a name
                project_count = project_count + 1
                print('loading Project: '+ row[2])
                if row[1].strip().startswith('http'):
                    url = row[1].strip()
                else:
                    url = 'http://'+row[1].strip()
                title = row[2]
                finished_editing = row[3]
                organization_name = row[4]
                kind = row[5]
                cms = row[6]
                framework = row[7]
                responsive = row[8]
                mobile = row[9]
                mapping = row[10]
                status = row[11]
                organization_type = row[12]
                area_city = row[13]
                area_state = row[14]
                area_country = row[15]
                description_en = row[16]
                description_de = row[17]
                description_fr = row[18]
                description_ar = row[19]
                logo = row[20]
                hashtags = row[21]
                categories = row[22]
                orgacontact_name = row[23]
                orgacontact_email = row[24]
                orgacontact_language = row[25]
                contact_email = row[26]
                contact_phone = row[27]
                contact_socialmedia_fb = row[28]
                contact_socialmedia_twitter = row[29]
                contact_adress_street = row[30]
                contact_adress_housenr = row[31]
                contact_adress_postalcode = row[32]
                contact_adress_city = row[33]
                contact_adress_state = row[34]
                contact_adress_country = row[35]
                code_repository = row[36]
                programming_languages = row[37]
                languages = row[38]
                code_license = row[39]
                releasedate = row[40]
                last_update_of_table = row[41]
                software_development_needs = row[42]
                flyer = row[44]

                #### Check, if project existent in database, If so, update the
                #### fields, if not, create it
                newPro = None
                try:
                    newPro = Project.objects.get(title=title)
                except ObjectDoesNotExist:
                    newPro = Project(title=title)

                newPro.url = url
                newPro.area_city = area_city
                newPro.area_country = area_country
                newPro.area_state = area_state

                newPro.contact_address_city = contact_adress_city
                newPro.contact_address_country = contact_adress_country
                newPro.contact_address_housenr = contact_adress_housenr
                newPro.contact_address_street = contact_adress_street
                newPro.contact_address_zip = contact_adress_postalcode
                newPro.contact_socialmedia_fb = contact_socialmedia_fb
                newPro.contact_socialmedia_twitter = contact_socialmedia_twitter
                newPro.contact_telephone = contact_phone

                newPro.organisation_name = organization_name
                newPro.description_de = description_de
                newPro.description_en = description_en
                newPro.description_fr = description_fr
                newPro.description_ar = description_ar

                if status.strip().lower() == 'inactive':
                    newPro.status = 0
                elif status.strip().lower() == 'active' or status.strip().lower() == 'läuft':
                    newPro.status = 1
                elif status.strip().lower() == 'in progress':
                    newPro.status = 2
                else:
                    if status.strip() != '':
                        print('GOT UNRECOGNIZED STATUS: ' + status + ' , Project id: ' + row[0])
                    newPro.status = 3
                newPro.logo = logo.strip() if logo.strip() != '' else models.default_logo()
                newPro.save()

                for singleKind in kind.split(','):
                    if singleKind.strip() == '':
                        continue

                    dbKindResult = Kind.objects.filter(name=singleKind.strip().lower())
                    kindResult = None
                    if len(dbKindResult) == 0:
                        print('GOT UNRECOGNIZED KIND: '+ singleKind + ' , Project id: ' + row[0])
                        kindResult = Kind.objects.get(name='unspecified')
                    else:
                        kindResult = dbKindResult.first()
                    newPro.kind.add(kindResult)


                languagesArray = languages.lower().split(',')

                for language in languagesArray:
                    if language.strip() == '':
                        continue
                    langFromDb = None
                    try:
                        langFromDb = PageLanguage.objects.get(name=language.strip)
                    except ObjectDoesNotExist:
                        try:
                            langFromDb = PageLanguage.objects.get(abbreviation=language.strip())
                        except ObjectDoesNotExist:
                            try:
                                langFromDb = PageLanguage.objects.get(alternatives__icontains=language.strip())
                            except ObjectDoesNotExist:
                                print('GOT UNRECOGNIZED LANGUAGE: ' + language.strip() + ' , Project id: ' + row[0])
                                langFromDb = PageLanguage.objects.get(name='unknown')

                    newPro.languages.add(langFromDb)

                programming_languages = programming_languages.strip().lower()
                prog_arr = programming_languages.split(',')
                for prog_lang in prog_arr:
                    if prog_lang.strip() != '':
                        dbPlang = None
                        try:
                            dbPlang = ProgrammingLanguage.objects.get(name=prog_lang.strip().lower)
                        except ObjectDoesNotExist:
                            dbPlang = ProgrammingLanguage(name=prog_lang.strip().lower())
                            dbPlang.save()
                        newPro.programming_languages.add(dbPlang)

                catList = categories.split(',')
                if len(catList) > 0 and categories.strip != '':
                    for currentCat in catList:
                        if currentCat.strip() != '' :
                            cat = Category.objects.all().filter(name=currentCat.strip())
                            if len(cat) == 0:
                                print('GOT UNRECOGNIZED CATEGORY : ' + currentCat + ' , Project id: ' + row[0])
                            else:
                                for currentCat in cat:
                                    if len(newPro.categories.all().filter(pk=currentCat.pk)) == 0 :
                                        newPro.categories.add(currentCat)
                                    if currentCat.parent != None and len(newPro.categories.all().filter(pk=currentCat.parent.pk)) == 0:
                                        newPro.categories.add(currentCat.parent)


                assign_perm('change_project', editors, newPro)

                newPro.save()
            else:
                print("GOT NO TITLE in Project id:  " + row[0] )
        print("saved " + str(project_count) + " Projects!")

def getCategoriesCsvData():
    categories_url = 'https://docs.google.com/spreadsheets/d/1L9huhE5AFTwjurwd_dGBasU9Qe0g8gFSmpiMrggxEKA/pub?gid=1240095638&single=true&output=csv'
    response = requests.get(categories_url)
    assert response.status_code == 200, 'Wrong status code'
    return response.content.decode('utf-8')

def getProjectCsvData():
   response = requests.get('https://docs.google.com/spreadsheets/d/1L9huhE5AFTwjurwd_dGBasU9Qe0g8gFSmpiMrggxEKA/pub?gid=1986004337&single=true&output=csv')
   assert response.status_code == 200, 'Wrong status code'
   return response.content.decode('utf-8')
   #with open("output.cvs", "w") as text_file:
    #   print(response.content.decode('utf-8'))
     #  text_file.write(response.content.decode('utf-8'))

   #text_file.close()
