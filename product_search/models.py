import requests
from enum import Enum
from tempfile import NamedTemporaryFile

from django.core.files import File
from django.db import models

class CountryChoice(Enum):
    US = "US"
    KR = "Korea"
    JP = "Japan"

import os

def get_image_path(instance, filename):
    return os.path.join('product_photos', str(instance.id), filename)

class Brand(models.Model):
    name = models.CharField(max_length=600)
    country = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in CountryChoice], blank=True)
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=600)
    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=600)
    img = models.ImageField(upload_to=get_image_path, max_length=600, blank=True)
    imglink = models.URLField(max_length=1000, blank=True)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    def __str__(self):
        return self.name

    def download_img():
        img_temp = NamedTemporaryFile(delete=True)
        if self.imglink and not self.img:
            img_response = requests.get(self.imglink)
            if img_response.status_code == 200:
                img_temp.write(img_response.content)
                img_temp.flush()
                self.img.save(f"{self.brand}-{self.name}-img", File(img_temp))
        self.save()
