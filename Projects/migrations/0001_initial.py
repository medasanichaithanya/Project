# Generated by Django 4.2 on 2023-04-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('age', models.FloatField(blank=True, null=True)),
                ('waist', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
