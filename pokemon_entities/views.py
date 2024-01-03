import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=localtime(), disappeared_at__gte=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
            add_pokemon(
                folium_map, pokemon.latitude,
                pokemon.longitude,
                request.build_absolute_uri(pokemon.pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.pokemon.image.url),
                'title_ru': pokemon.pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    request_pokemons = PokemonEntity.objects.filter(pokemon=pokemon_id)
    if request_pokemons.exists():
        pokemon1 = {
            "pokemon_id": request_pokemons.first().pokemon.id,
            "title_ru": request_pokemons.first().pokemon.title,
            "title_en": request_pokemons.first().pokemon.title_en,
            "title_jp": request_pokemons.first().pokemon.title_jp,
            "description": request_pokemons.first().pokemon.description,
            "img_url": request.build_absolute_uri(request_pokemons.first().pokemon.image.url),
            "entities": [
                {
                    "level": 15,
                    "lat": 55.753244,
                    "lon": 37.628423
                },
                {
                    "level": 24,
                    "lat": 55.743244,
                    "lon": 37.635423
                }
            ],
            # "next_evolution": {
            #     "title_ru": "Ивизавр",
            #     "pokemon_id": 2,
            #     "img_url": "https://vignette.wikia.nocookie.net/pokemon/images/7/73/002Ivysaur.png/revision/latest/scale-to-width-down/200?cb=20150703180624&path-prefix=ru"
            # },
            "previous_evolution": {
                "title_ru": request_pokemons.first().pokemon.previous_evolution.title,
                "pokemon_id": request_pokemons.first().pokemon.previous_evolution.id,
                "img_url": request.build_absolute_uri(request_pokemons.first().pokemon.previous_evolution.image.url)
            }
        }
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in request_pokemons:
        add_pokemon(
            folium_map, pokemon.latitude,
            pokemon.longitude,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon1
    })
