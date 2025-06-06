from django.contrib import admin

# Register your models here.

#admin.site.register()
from .models import PopularMovie
from .models import Testimonial
from .models import AboutTMDb

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author', 'text')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)




@admin.register(PopularMovie)
class PopularMovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    list_editable = ('is_active',)





@admin.register(AboutTMDb)
class AboutTMDbAdmin(admin.ModelAdmin):
    list_display   = ('title', 'is_active')
    list_filter    = ('is_active',)
    search_fields  = ('title', 'text')
    list_editable  = ('is_active',)
    readonly_fields = ()