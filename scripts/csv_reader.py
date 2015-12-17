import csv

def reader():
   with open('output.cvs', 'rb') as out:
       reader = csv.reader(out, delimiter=',', quotechar='"')
       for line in reader:
           yield line
