import json
import re
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from product_search.models import *

GOOGLE_IMG_API_URL = 'https://customsearch.googleapis.com/customsearch/v1'


class Command(BaseCommand):
    help = 'Loads skincare products into db'

    def load_ingredient_data(self):
        """
        ETL ingredient data
        """
        self.stdout.write("attempting fetch - ing api")
        ing_response = requests.get('https://skincare-api.herokuapp.com/ingredients')
        if ing_response.status_code != 200:
            self.stderr.write(ing_response.body)
            raise CommandError(f"load_product failed - ing_response request failed status_code={ing_response.status_code}")
        self.stdout.write("successful fetch - ing api")

        self.stdout.write("starting ingredient data load")
        ingdata = ing_response.json()

        for ingredient in ingdata:
            ing, created = Ingredient.objects.get_or_create(
                name = ingredient['ingredient']
            )
        self.stdout.write("successfully loaded ingredient data")

    def load_product_data(self):
        """
        ETL product data
        """
        self.stdout.write("attempting fetch - product api")
        product_response = requests.get('https://skincare-api.herokuapp.com/products')
        if product_response.status_code != 200:
            self.stderr.write(product_response.text)
            raise CommandError(f"load_product failed - product_response request failed status_code={product_response.status_code}")
        self.stdout.write("successful fetch - product api")

        self.stdout.write("starting product data load")
        productdata = product_response.json()

        for product in productdata:
            brand_obj, brand_created = Brand.objects.get_or_create(
                name=product['brand']
            )

            product_name = re.sub('cr\u032cme', 'creme', product['name'])

            product_obj, product_created = Product.objects.get_or_create(
                name=product_name,
                brand=brand_obj
            )

            if product_created:
                img_query = {
                    "key": settings.API_KEY,
                    "cx": settings.CX,
                    "searchType": "image",
                    "num": 1,
                    "q": f"{product['brand']} {product_name}"
                }

                img_response = requests.request("GET", GOOGLE_IMG_API_URL, params=img_query)

                if img_response.status_code == 200:
                    imgdata = img_response.json()
                    if "items" in imgdata:
                        imglink = imgdata["items"][0].get("link")
                        product_obj.imglink = imglink
                        product_obj.save()
                    else:
                        self.stderr.write(json.dumps(imgdata, indent=4))
                elif img_response.status_code == 429:
                    self.stderr.write(img_response.text)
                    raise CommandError(f"load_product failed - google image api resource exhausted")
                else:
                    self.stderr.write(product_response.text)
                    raise CommandError(f"load_product failed - product_response request failed status_code={product_response.status_code}")

            for ingredient in product['ingredient_list']:
                ing_obj, ing_created = Ingredient.objects.get_or_create(name=ingredient)
                if ing_created:
                    self.stderr.write(f"{ing_obj} was created from productdata")
                product_obj.ingredients.add(ing_obj)
                product_obj.save()


    def handle(self, *args, **options):
        self.load_ingredient_data()
        self.load_product_data()
