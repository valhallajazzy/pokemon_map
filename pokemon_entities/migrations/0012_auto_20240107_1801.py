# Generated by Django 3.1 on 2024-01-07 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_auto_20240107_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemons_on_map', to='pokemon_entities.pokemon', verbose_name='Вид'),
        ),
    ]
