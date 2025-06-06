# файл: main/recommender.py
import os
import time
import pickle

import pandas as pd
import requests
from sklearn.preprocessing import LabelEncoder

# TMDb API key — храните его где-нибудь в настройках,
# но для примера мы просто жестко пишем его здесь
API_KEY = '562390045e557970f5b5e10ad05730a1'

# Путь к файлу-кэшу. В репозитории / на проде появится этот файл и будет храниться рядом.
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'movies_cache.pkl')

# Маппинг категорий длительности (русские лейблы → числовые)
RUNTIME_LABELS = ['короткий', 'средний', 'длинный']

# Глобальные переменные, которые будут инициализированы при первом импорте:
_movies_df = None
_unique_genres = None
_runtime_encoder = None


def load_movies_from_tmdb(api_key: str, pages: int = 40) -> pd.DataFrame:
    """
    Если CACHE_FILE существует, просто возвращает pd.DataFrame из него.
    Иначе скачивает первые `pages` страниц popular → сохраняет runtime/rating →
    кладёт всё в pickle и возвращает DataFrame.
    """
    global _movies_df

    # Если уже загружено в памяти, не тратим время дважды
    if _movies_df is not None:
        return _movies_df

    # Если есть локальный кеш — считываем его
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            _movies_df = pickle.load(f)
        return _movies_df

    # Иначе: качаем заново
    movies_list = []
    for page in range(1, pages + 1):
        url = (
            f'https://api.themoviedb.org/3/discover/movie'
            f'?sort_by=popularity.desc'
            f'&api_key={api_key}'
            f'&page={page}'
            f'&language=ru'
        )
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json().get('results', [])
            movies_list.extend(data)
        else:
            print(f"Ошибка загрузки page={page} с TMDb API")
        time.sleep(0.1)  # чтобы не забанили за слишком частые запросы

    # Теперь для каждого фильма вытягиваем runtime и рейтинг
    for m in movies_list:
        movie_id = m.get('id')
        detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ru'
        resp = requests.get(detail_url)
        if resp.status_code == 200:
            jd = resp.json()
            m['runtime'] = jd.get('runtime', 0)
            m['rating'] = jd.get('vote_average', 0)
        else:
            m['runtime'] = 0
            m['rating'] = 0
        time.sleep(0.1)

    # Формируем DataFrame
    df = pd.DataFrame(movies_list)
    if not df.empty:
        df = df[['id', 'title', 'popularity', 'genre_ids', 'runtime', 'rating']]
        df.columns = ['movieId', 'title', 'popularity', 'genres', 'runtime', 'rating']
    else:
        df = pd.DataFrame(columns=['movieId', 'title', 'popularity', 'genres', 'runtime', 'rating'])

    # Сохраняем в файл-кэш
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(df, f)

    _movies_df = df
    return _movies_df


def prepare_data(df: pd.DataFrame):
    """
    На вход DataFrame с колонками ['movieId','title','popularity','genres','runtime','rating'].

    Добавляет:
     - столбец "genre_vector" — бинарный вектор наличия каждого жанра
     - столбец "popularity_norm" — нормированная популярность (от 0 до 1)
     - столбец "runtime_category" — целое 0/1/2 (короткий/средний/длинный)
    Возвращает (df, unique_genres, runtime_encoder).
    """
    global _unique_genres, _runtime_encoder

    # Алгоритм: unique_genres = список всех жанров, встречающихся в 'genres'
    unique_genres = sorted({
        g
        for row in df['genres']
        for g in (row if isinstance(row, list) else [row])
    })
    df['genre_vector'] = df['genres'].apply(
        lambda gl: [1 if g in gl else 0 for g in unique_genres]
    )

    # нормализуем колонку 'popularity' в [0,1]
    df['popularity_norm'] = df['popularity'] / df['popularity'].max()

    # категориальный столбец runtime: 'короткий','средний','длинный'
    df['runtime_cat_str'] = pd.cut(
        df['runtime'],
        bins=[0, 80, 130, float('inf')],
        labels=RUNTIME_LABELS
    )
    # Преобразуем в числа 0/1/2
    encoder = LabelEncoder()
    df['runtime_cat'] = encoder.fit_transform(df['runtime_cat_str'])

    _unique_genres = unique_genres
    _runtime_encoder = encoder

    return df, unique_genres, encoder


def get_recommendations(genre_ids: list[int],
                        pop_thresh: float,
                        runtime_cat: int) -> list[tuple[str, float]]:
    """
    Возвращает список кортежей (title, rating) отсортированных по убыванию рейтинга,
    удовлетворяющих:
      - жанровый вектор movie_genres пересекается с genre_ids (хотя бы один общий жанр)
      - popularity_norm >= pop_thresh
      - runtime_cat равно указанному
    """
    global _movies_df, _unique_genres, _runtime_encoder

    # Убедимся, что данные уже загружены и подготовлены:
    if _movies_df is None:
        df_raw = load_movies_from_tmdb(API_KEY, pages=5)
        df_raw, _unique_genres, _runtime_encoder = prepare_data(df_raw)

    df = _movies_df.copy()

    # Построим единичный вектор пользователя:
    user_vec = [1 if g in genre_ids else 0 for g in _unique_genres]

    recs = []
    for _, row in df.iterrows():
        mv_vec = row['genre_vector']
        score = sum(u * v for u, v in zip(user_vec, mv_vec))
        if score > 0 \
           and row['popularity_norm'] >= pop_thresh \
           and row['runtime_cat'] == runtime_cat:
            recs.append((row['title'], row['rating']))

    # Сортируем по убыванию рейтинга (2-й элемент в кортеже)
    recs.sort(key=lambda x: x[1], reverse=True)
    return recs
