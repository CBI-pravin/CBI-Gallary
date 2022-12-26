# Generated by Django 4.1.3 on 2022-12-24 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='mygallary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=home.models.UploadToPathAndRename('media/'))),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='myfolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('folder_created_date', models.DateTimeField(auto_now_add=True)),
                ('folder_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_owner', to=settings.AUTH_USER_MODEL)),
                ('photo', models.ManyToManyField(blank=True, related_name='photo', to='home.mygallary')),
            ],
        ),
    ]
