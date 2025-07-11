# Generated by Django 5.2 on 2025-05-01 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Merch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/')),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
