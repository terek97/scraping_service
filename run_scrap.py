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
                 'save_area=True&area=1&from=NEIGHBOURS&showClusters=true'),
    (habr, 'https://career.habr.com/vacancies?city_id=678&skills[]=446&type=all')
)

city = City.objects.filter(slug='moskva').first()
profession = Profession.objects.filter(slug='python').first()

vacancies, errors = [], []
for func, url in parsers:
    v, e = func(url)
    vacancies += v
    errors += e

for vacancy in vacancies:
    v = Vacancy(**vacancy, city=city, profession=profession)
    try:
        obj, created = Vacancy.objects.get_or_create(**vacancy, city=city, profession=profession)
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors)

