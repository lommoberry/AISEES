# Generated by Django 4.2.10 on 2024-03-22 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_researchitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researchitem',
            name='country',
        ),
        migrations.AddField(
            model_name='researchitem',
            name='country',
            field=models.ManyToManyField(blank=True, to='myapp.country'),
        ),
    ]
