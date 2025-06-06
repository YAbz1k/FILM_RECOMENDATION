import requests  # остался, если где-то нужен
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Testimonial, PopularMovie, AboutTMDb
from .recommender import get_recommendations  # <-- наш новый модуль

# Маппинг имён жанров TMDb → их ID
GENRE_NAME_TO_ID = {
    'action': 28,
    'adventure': 12,
    'animation': 16,
    'comedy': 35,
    'crime': 80,
    'documentary': 99,
    'drama': 18,
    'family': 10751,
    'fantasy': 14,
    'history': 36,
    'horror': 27,
    'music': 10402,
    'mystery': 9648,
    'romance': 10749,
    'science fiction': 878,
    'scifi': 878,
    'tv movie': 10770,
    'thriller': 53,
    'war': 10752,
    'western': 37,
}


def index(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    popular_movies = PopularMovie.objects.filter(is_active=True)
    return render(request, 'main/index.html', {
        'testimonials': testimonials,
        'popular_movies': popular_movies,
    })


def about(request):
    tmdb_blocks = AboutTMDb.objects.filter(is_active=True)
    return render(request, 'main/about.html', {
        'tmdb_blocks': tmdb_blocks
    })


def form(request):
    recommendations = None

    if request.method == 'POST':
        # 1) Жанры → ID
        raw = request.POST.get('genres', '')
        tokens = [t.strip().lower() for t in raw.replace(',', ' ').split()]
        genre_ids = [GENRE_NAME_TO_ID[t] for t in tokens if t in GENRE_NAME_TO_ID]

        # 2) Популярность (да/нет) → 1 или 0
        raw_pop = request.POST.get('popularity', '').lower()
        pop_thresh = 1.0 if raw_pop == 'да' else 0.0

        # 3) Длительность
        raw_rt = request.POST.get('runtime', '').lower()
        if raw_rt == 'короткий':
            rt_cat = 0
        elif raw_rt == 'длинный':
            rt_cat = 2
        else:
            rt_cat = 1  # «средний» по умолчанию

        # 4) Собственно, получаем рекомендации из нашего модуля
        recs = get_recommendations(genre_ids, pop_thresh, rt_cat)
        recommendations = recs

    return render(request, 'main/form.html', {
        'recommendations': recommendations
    })



def about(request):
    tmdb_blocks = AboutTMDb.objects.filter(is_active=True)
    return render(request, 'main/about.html', {
        'tmdb_blocks': tmdb_blocks
    })