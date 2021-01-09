# Generated by Django 3.1.4 on 2021-01-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AddField(
            model_name='post',
            name='title_image',
            field=models.ImageField(blank=True, upload_to='blog/title_image/', verbose_name='title_image'),
        ),
    ]
