import folium
import json

from django.shortcuts import get_object_or_404
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
    local_time = localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=local_time, disappeared_at__gte=local_time)
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

    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons_for_map = requested_pokemon.pokemons.all()

    previous_evolution_pokemon = requested_pokemon.previous_evolution
    next_evolution_pokemon = requested_pokemon.previous_evolutions.all().first()

    pokemon_info = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
    }
    if previous_evolution_pokemon:
        pokemon_info["previous_evolution"] = {
            "title_ru": previous_evolution_pokemon.title,
            "pokemon_id": previous_evolution_pokemon.id,
            "img_url": request.build_absolute_uri(previous_evolution_pokemon.image.url)
        }
    if next_evolution_pokemon:
        pokemon_info["next_evolution"] = {
            "title_ru": next_evolution_pokemon.title,
            "pokemon_id": next_evolution_pokemon.id,
            "img_url": request.build_absolute_uri(next_evolution_pokemon.image.url)
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons_for_map:
        add_pokemon(
            folium_map, pokemon.latitude,
            pokemon.longitude,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
