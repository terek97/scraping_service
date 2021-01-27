from django.contrib import admin
from .models import City, Profession, Vacancy, Error

# Register your models here.
admin.site.register(City)
admin.site.register(Profession)
admin.site.register(Vacancy)
admin.site.register(Error)
