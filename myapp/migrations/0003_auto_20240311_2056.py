# Generated by Django 4.2.10 on 2024-03-11 20:56

from django.db import migrations

def add_countries(apps, schema_editor):
    Country = apps.get_model('myapp', 'Country')
    countries = ['Albania', 'Bosnia and Herzegovina', 'Bulgaria','Croatia','Kosovo','Moldova','Montenegro','North Macedonia','Romania','Serbia','Slovenia']
    for name in countries:
        Country.objects.create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_country_researcher'),
    ]

    operations = [
        migrations.RunPython(add_countries),
    ]
