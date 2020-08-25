from django.contrib import admin

# Register your models here.
from product_search.models import *

admin.site.register(Brand)
admin.site.register(Ingredient)
admin.site.register(Product)
