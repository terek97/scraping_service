import jsonfield as jsonfield
from django.db import models
from .utils import make_slug


def default_urls():
    return {'headhunter': '', 'habr': ''}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название населенного пункта',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Название населенного пункта"
        verbose_name_plural = "Название населенных пунктов"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_slug(str(self.name))
            super().save(*args, **kwargs)


class Profession(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ключевой навык',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Ключевой навык"
        verbose_name_plural = "Ключевые навыки"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_slug(str(self.name))
            super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии', unique=True)
    company = models.CharField(max_length=250, verbose_name='Компания', unique=True)
    description = models.TextField(verbose_name='Описание вакансии', unique=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE,
                                   verbose_name='Ключевой навык')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE,
                                   verbose_name='Ключевой навык')
    url_data = jsonfield.JSONField(default=default_urls())
    
    class Meta():
        unique_together = ('city', 'profession')
