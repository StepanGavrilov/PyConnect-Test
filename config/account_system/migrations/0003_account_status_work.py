# Generated by Django 3.1.4 on 2021-01-11 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_system', '0002_account_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='status_work',
            field=models.CharField(blank=True, max_length=32, verbose_name='Status work'),
        ),
    ]
