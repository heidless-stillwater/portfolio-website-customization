# Generated by Django 3.2.12 on 2022-03-03 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='images')),
            ],
            options={
                'verbose_name': 'Hero',
                'verbose_name_plural': 'Hero',
            },
        ),
    ]
