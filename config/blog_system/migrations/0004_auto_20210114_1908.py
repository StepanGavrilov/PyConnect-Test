# Generated by Django 3.1.4 on 2021-01-14 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_system', '0003_auto_20210113_0013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created',), 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
    ]
