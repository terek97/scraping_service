import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.scrap import *
from scraping.models import City

parsers = (
    (headhunter, 'https://hh.ru/search/vacancy?clusters=true&text=python&enable_snippets=true&L_'
                 'save_area=True&area=79&from=NEIGHBOURS&showClusters=true'),
    (jooble, 'https://ru.jooble.org/SearchResult?rgns=Саратов&ukw=python')
)

city = City.objects.filter(slug='saratov')

vacancies, errors = [], []
for func, url in parsers:
    v, e = func(url)
    vacancies += v
    errors += e

h = codecs.open('parsed.json', 'w', 'utf-8')
h.write(str(vacancies))
h.close()
