from django.contrib import admin
from .models import City, Vacancy
from .models import Profession

# Register your models here.
admin.site.register(City)
admin.site.register(Profession)
admin.site.register(Vacancy)
