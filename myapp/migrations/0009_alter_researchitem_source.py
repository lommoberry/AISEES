# Generated by Django 4.2.10 on 2024-03-22 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_researchitem_country_researchitem_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchitem',
            name='source',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
