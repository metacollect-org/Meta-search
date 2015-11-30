import csv

with open('output.cvs', 'rb') as out:
    reader = csv.reader(out, delimiter=',', quotechar='"')
    for i,line in enumerate(reader):
        print i,'\t','|'.join(line)
