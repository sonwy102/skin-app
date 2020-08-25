from django.conf import settings
from django.db.models.functions import Concat
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render

from product_search.forms import SearchForm
from product_search.models import *
import requests

def search(request):
    """
    A view that fuzzy-searches products, brands, ingredients given user input
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_input = form.cleaned_data['search_input']

            p = set(Product.objects.annotate(
                querystr=Concat(
                    F('brand__name'),
                    F('name'),
                    F('ingredients__name'))
                ).filter(querystr__icontains=search_input))

            return render(request, 'searched.html', {'productdata': p})
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
