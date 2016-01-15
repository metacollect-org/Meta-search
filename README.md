# Meta-search

##What is Meta-search?  
Meta-search is a Django Web project.   
It's part of the 'Ini 2.0 Data Science: Hacking for refugees' course.   
Goal: A database filled with refugee helping projects.  


##Our project
Die Hilfsangebote, Informationen, Initiativen und Plattformen für Geflüchtete in Deutschland sind zahlreich - einen Überblick zu schaffen wird immer schwieriger. Wir möchten alle unterstützen, die sich informieren, integrieren oder helfen möchten. In einer übersichtlichen Plattform soll eine filterbare, mehrsprachige Darstellung der bestehenden Projekte in Deutschland entwickelt werden, sodass die Suche nach den benötigten Informationen nur noch wenige Klicks benötigt. Insbesondere sollen dadurch Newcomer in ihrem Alltag unterstützt werden.  

Das Projekt wird im Rahmen eines Seminars an der TU Berlin umgesetzt. Gemeinsam arbeiten ca. 10 Studierende und bringen ihre vielseitigen und unterschiedlichen Qualitäten und Fachkompetenzen aktiv in die Teamarbeit mit ein. Durch diese interdisziplinäre Zusammenarbeit können mit studentischem Engangement einfache Lösungen für gesellschaftliche Probleme gefunden werden.  


##Guide to install Meta-search

1. Install Python 3
2. Install Pip
3. Install Git
4. Download this repo (`$git clone https://github.com/patreu22/Meta-search/`)
5. Install the neccessary dependencies with `pip install -r requirements.txt`
6. Download elasticsearch 1.7.4 : `wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.4.zip`, unpack anywhere you like, and run it.
6. Run `$python manage.py migrate`
7. Run `$python manage.py rebuild_index` to initalise the elasticsearch instance and re-run to copy changes from db to elastic
8. Run `$python manage.py load_csv_data` to Download the Project data and integrate it into the database
9. Start Meta-Search with $python manage.py runserver locally. For making it accessible over your IP for everybody use $python manage.py runserver 0.0.0.0:8000  
10. You can see the result of the project if you access localhost:8000 in your browser.