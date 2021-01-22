from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):

    qs = []
    form = FindForm()
    city = request.GET.get('city')
    profession = request.GET.get('profession')

    if city or profession:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if profession:
            _filter['profession__slug'] = profession
        qs = Vacancy.objects.filter(**_filter)

    context = {'object_list': qs, 'form': form}

    return render(request, 'scraping/index.html', context)

