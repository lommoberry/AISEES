# Generated by Django 4.2.10 on 2024-03-18 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0004_alter_researcher_address_alter_researcher_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher',
            name='email',
        ),
        migrations.AddField(
            model_name='researcher',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='researcher',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='address',
            field=models.TextField(),
        ),
    ]
