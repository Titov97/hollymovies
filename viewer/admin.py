from django.contrib import admin

# Register your models here.
from viewer.models import Movie, Genre

admin.site.register(Movie)
admin.site.register(Genre)
