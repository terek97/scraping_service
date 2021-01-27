import codecs
import os, sys

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.scrap import *
from scraping.models import City, Profession, Vacancy, Error

parsers = (
    (headhunter, 'https://hh.ru/search/vacancy?clusters=true&text=python&enable_snippets=true&L_'
                 'save_area=True&area=79&from=NEIGHBOURS&showClusters=true'),
    (jooble, 'https://ru.jooble.org/SearchResult?rgns=Саратов&ukw=python')
)

city = City.objects.filter(slug='saratov').first()
profession = Profession.objects.filter(slug='python').first()

vacancies, errors = [], []
for func, url in parsers:
    v, e = func(url)
    vacancies += v
    errors += e

for vacancy in vacancies:
    v = Vacancy(**vacancy, city=city, profession=profession)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors)

