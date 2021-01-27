import requests
from bs4 import BeautifulSoup as bs

__all__ = ('headhunter', 'jooble')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329'}


def headhunter(url):
    vacancies = []
    errors = []

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        main_tag = soup.find('div', attrs={'class': 'vacancy-serp'})
        if main_tag:
            tag_list = main_tag.find_all('div', attrs={'class': 'vacancy-serp-item'})
            for tag in tag_list:
                title = tag.a.text
                href = tag.a['href']
                company = tag.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
                content = tag.find('div', attrs={'class': 'g-user-content'}).text
                vacancies.append({'url': href, 'title': title, 'company': company,
                                  'description': content})
                if not (title and href and company and content):
                    errors.append({'url': url, 'title': 'Something wrong inside tag list'})

        else:
            errors.append({'url': url, 'title': 'Main div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page does not response'})
    return vacancies, errors


def jooble(url):
    vacancies = []
    errors = []

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        main_tag = soup.find('div', attrs={'class': '_70404'})
        if main_tag:
            tag_list = main_tag.find_all('article', attrs={'class': '_31572 _07ebc'})

            for tag in tag_list:
                title = tag.find('span', attrs={'class': '_4ef07 _32b89 _13855'}).text
                href = f"https://ru.jooble.org{tag.a['href']}"
                company = tag.find('div', attrs={'class': 'caption _8d375'}).text
                content = tag.find('div', attrs={'class': '_0b1c1'}).text
                vacancies.append({'url': href, 'title': title, 'company': company,
                                  'description': content})
                if not (title and href and company and content):
                    errors.append({'url': url, 'title': 'Something wrong inside tag list'})

        else:
            errors.append({'url': url, 'title': 'Main div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page does not response'})
    return vacancies, errors
