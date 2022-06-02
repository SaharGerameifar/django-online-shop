# Generated by Django 3.2.12 on 2022-04-06 20:22

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20220401_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('link', models.URLField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='products_slider/%Y/%m/%d/')),
            ],
        ),
    ]