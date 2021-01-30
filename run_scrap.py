import codecs
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.scrap import *
from scraping.models import City, Profession, Vacancy, Error, Url

User = get_user_model()

parsers = (
    (headhunter, 'headhunter'),
    (habr, 'habr')
)


def get_settings():
    qs = User.objects.filter(is_active=True).values()
    setting_list = set((q['city_id'], q['profession_id']) for q in qs)
    return setting_list


def get_urls(_setting):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['profession_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _setting:
        tmp = {'city': pair[0], 'profession': pair[1], 'url_data': url_dict[pair]}
        urls.append(tmp)
    return urls


q = get_settings()
url_list = get_urls(q)

vacancies, errors = [], []
for data in url_list:
    for func, key in parsers:
        url = data['url_data'][key]
        v, e = func(url, city=data['city'], profession=data['profession'])
        vacancies += v
        errors += e

for vacancy in vacancies:
    try:
        obj, created = Vacancy.objects.get_or_create(**vacancy)
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors)

