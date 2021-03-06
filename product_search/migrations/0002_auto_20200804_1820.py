# Generated by Django 3.0.8 on 2020-08-04 18:20

from django.db import migrations, models
import product_search.models


class Migration(migrations.Migration):

    dependencies = [
        ('product_search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, max_length=600, upload_to=product_search.models.get_image_path),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=600),
        ),
    ]
