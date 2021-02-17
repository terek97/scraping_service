import asyncio
import os
import sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.scrap import *
from scraping.models import Vacancy, Error, Url


User = get_user_model()
vacancies, errors = [], []

parsers = (
    (headhunter, 'headhunter'),
    (habr, 'habr')
)


async def main(value):
    func, url, city, profession = value
    job, err = await loop.run_in_executor(None, func, url, city, profession)
    vacancies.extend(job)
    errors.extend(err)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
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


settings = get_settings()
url_list = get_urls(settings)


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['profession'])
             for data in url_list
             for func, key in parsers
             ]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()

for vacancy in vacancies:
    try:
        obj, created = Vacancy.objects.get_or_create(**vacancy)
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors)

