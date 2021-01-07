# Generated by Django 3.1.4 on 2021-01-05 18:41

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='Username')),
                ('email', models.EmailField(db_index=True, max_length=32, unique=True, verbose_name='E-mail')),
                ('first_name', models.CharField(blank=True, max_length=32, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=32, verbose_name='Last name')),
                ('gender', models.CharField(blank=True, choices=[('f', 'Female'), ('m', 'Male')], max_length=2, verbose_name='Gender')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Age')),
                ('about_me', models.CharField(blank=True, max_length=1024, verbose_name='About me')),
                ('location', models.CharField(blank=True, max_length=32, verbose_name='Location')),
                ('avatar', models.ImageField(blank=True, default='../static/img/account/noimage.png', upload_to='account/avatar/', verbose_name='Avatar')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last login')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
