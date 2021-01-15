from django.db import models
from .utils import make_slug


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название населенного пункта',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Название населенного пункта"
        verbose_name_plural = "Название населенных пунктов"

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = make_slug(self.name)
            super().save()


class Profession(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название должности',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Название должности"
        verbose_name_plural = "Название должностей"

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = make_slug(self.name)
            super().save()


class Vacancy(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=250, verbose_name='')
    company = models.CharField(max_length=250, verbose_name='')
    description = models.TextField(verbose_name='')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='')
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE,
                                   verbose_name='')
