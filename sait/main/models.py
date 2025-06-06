from django.db import models


class Testimonial(models.Model):
    author = models.CharField("Автор", max_length=100)
    text = models.TextField("Текст отзыва")
    is_active = models.BooleanField("Показывать на сайте", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        # Отображается в списке админки
        return f"{self.author}: {self.text[:30]}…"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']




class PopularMovie(models.Model):
    title = models.CharField("Название фильма", max_length=100)
    image = models.ImageField("Постер", upload_to='popular_movies/')
    is_active = models.BooleanField("Показывать на сайте", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Популярный фильм"
        verbose_name_plural = "Популярные фильмы"




# 💡 ДОБАВЛЯЕМ МОДЕЛЬ "О TMDb"
class AboutTMDb(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="about_tmdb/")
    is_active = models.BooleanField("Показывать на сайте", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блок О TMDb"
        verbose_name_plural = "Блоки О TMDb"