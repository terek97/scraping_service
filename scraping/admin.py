from django.contrib import admin
from .models import City, Profession, Vacancy

# Register your models here.
admin.site.register(City)
admin.site.register(Profession)
admin.site.register(Vacancy)
