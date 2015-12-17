import download_cvs
import csv_reader
from datetime import datetime
from document import Document
import time

download_cvs.get()
data = csv_reader.reader()
# print category names
for i, cat in enumerate(data.next()):
   print i, cat

for line in data:
   doc = Document(meta={'id': line[0]},
                  title=line[1],
                  area=line[6],
                  description=line[8],
                  categories=line[11],
                  languages=line[27],
                  timestamp=datetime.now(),
                  releasedate=line[31],
                  entrydate=line[32])
   doc.save()
   time.sleep(1)
