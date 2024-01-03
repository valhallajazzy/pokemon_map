from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Вид на английском')
    image = models.ImageField(null=True, blank=True, upload_to='pokemons_images')
    description = models.TextField(verbose_name='Описание')
    title_en = models.CharField(max_length=200, verbose_name='Вид на английском')
    title_jp = models.CharField(max_length=200, verbose_name='Вид на японском')
    previous_evolution = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL,
                                           related_name='evolution', verbose_name='Из кого эволюционирует')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Появляется')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Исчезает')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Атака')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title} {self.id}'