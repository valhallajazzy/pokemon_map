# Generated by Django 3.1.14 on 2024-01-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_pokemon_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Lat')),
                ('longitude', models.FloatField(verbose_name='Lon')),
            ],
        ),
    ]
