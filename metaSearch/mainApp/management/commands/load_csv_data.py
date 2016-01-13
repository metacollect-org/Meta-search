from django.core.management.base import BaseCommand
import requests
# import StringIO
import csv
from mainApp.models import Project, Category, ProgrammingLanguage
from django.core.exceptions import ObjectDoesNotExist

# csv table things
# 0: url
# 1: title
# 2: Online/ Offline
# 3: kind
# 4: Website
# 5: App
# 6: area
# 7: status
# 8: description
# 9: logo
# 10: hashtags
# 11: categories
# 12: orgacontact_name
# 13: orgacontact_email
# 14: orgacontact_language
# 15: contact_email
# 16: contact_phone
# 17: contact_socialmedia_fb
# 18: contact_socialmedia_twitter
# 19: contact_adress_street
# 20: contact_adress_housenr
# 21: contact_adress_postalcode
# 22: contact_adress_city
# 23: contact_adress_state
# 24: contact_adress_country
# 25: code_repository
# 26: programming_languages
# 27: languages
# 28: organization_type
# 29: organization_name
# 30: code_license
# 31: releasedate
# 32: entrydate
# 33: software_development_needs
# 34: random_generated_key


class Command(BaseCommand):
    args = 'No additional Arguments needed'
    help = 'Load the Refugee Project data from the Spreadsheet and put them in the Database'

    def handle(self, *args, **options):
        self.stdout.write("Hello World")
        # csvio = StringIO.StringIO(getCsvData())
        csvReader = csv.reader(getCsvData().split('\n'), delimiter=',')

        csvReader.__next__() # skip the first row, because these are the column names

        for row in csvReader:
            print('roundAgain')
            if row[1].strip() != '': # only take the ones, that have a name
                url = row[0]
                title = row[1]
                kind = row[3]
                area = row[6]
                status = row[7]
                description = row[8]
                logo = row[9]
                hashtags = row[10]
                categories = row[11]
                orgacontact_name = row[12]
                orgacontact_email = row[13]
                orgacontact_language = row[14]
                contact_email = row[15]
                contact_phone = row[16]
                contact_socialmedia_fb = row[17]
                contact_socialmedia_twitter = row[18]
                contact_adress_street = row[19]
                contact_adress_housenr = row[20]
                contact_adress_postalcode = row[21]
                contact_adress_city = row[22]
                contact_adress_state = row[23]
                contact_adress_country = row[24]
                code_repository = row[25]
                programming_languages = row[26]
                languages = row[27]
                organization_type = row[28]
                organization_name = row[29]
                code_license = row[30]
                releasedate = row[31]
                entrydate = row[32]
                software_development_needs = row[33]
                random_generated_key = row[34]

                newPro = None
                try:
                    newPro = Project.objects.get(title=title)
                except ObjectDoesNotExist:
                    newPro = Project(title=title)





                # newPro.title = title
                newPro.url = url
                newPro.area_city = area
                newPro.area_country = contact_adress_country
                newPro.area_state = contact_adress_state
                newPro.contact_address_city = contact_adress_city
                newPro.contact_address_country = contact_adress_country
                newPro.contact_address_housenr = contact_adress_housenr
                newPro.contact_address_street = contact_adress_street
                newPro.contact_address_zip = contact_adress_postalcode
                newPro.contact_socialmedia = contact_socialmedia_fb
                newPro.contact_telephone = contact_phone
                newPro.organisation_name = organization_name
                newPro.description = description

                if kind.strip().lower() == 'website' or kind.strip().lower() == 'webseite':
                    newPro.kind = 0
                elif kind.strip().lower()== 'app':
                    newPro.kind = 1
                elif kind.strip().lower() == 'map' or kind.strip().lower() == 'karte':
                    newPro.kind = 2
                elif kind.strip().lower() == 'facebook':
                    newPro.kind = 3
                else:
                    if kind.strip() != '':
                        print('NEW KIND FOUND! ' + kind)
                    newPro.kind = 4

                if status.strip().lower() == 'inactive':
                    newPro.status = 0
                elif status.strip().lower()== 'active' or status.strip().lower()== 'läuft':
                    newPro.status = 1
                elif status.strip().lower() == 'in progress':
                    newPro.status = 2
                else:
                    if status.strip() != '':
                        print('NEW status FOUND! ' + status)
                    newPro.status = 3

                newPro.logo = logo

                if languages.strip().lower().find('english') > -1:
                    newPro.languages = 0
                elif languages.strip().lower().find('german') > -1:
                    newPro.languages = 1
                else:
                    newPro.languages = 11

                newPro.needs = software_development_needs

                print(languages)
                newPro.save()
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
                if len(catList) > 1:
                    for currentCat in catList:
                        if currentCat.strip() != '' :
                            cat = None
                            try:
                                cat = Category.objects.get(name=currentCat.strip().lower())
                            except ObjectDoesNotExist:
                                print('Category not existent: ' + str(currentCat) + '... Creating it.')
                                cat = Category(name=currentCat)
                                cat.save()
                            newPro.categories.add(cat)

                print(newPro.categories)

                newPro.save()








def getCsvData():
   response = requests.get('https://docs.google.com/spreadsheet/ccc?key=102ZqoXXyzAJGD4SVEgbFaxvh4RvWvOfTMsYeLU8KYpY&output=csv')
   assert response.status_code == 200, 'Wrong status code'
   return response.content.decode('utf-8')
   #with open("output.cvs", "w") as text_file:
    #   print(response.content.decode('utf-8'))
     #  text_file.write(response.content.decode('utf-8'))

   #text_file.close()
