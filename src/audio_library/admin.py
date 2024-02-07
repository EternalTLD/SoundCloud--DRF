from django.contrib import admin

from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("title",)


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "release_date")
    list_display_links = ("user",)
    list_filter = ("user",)


@admin.register(models.Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "release_date")
    list_display_links = ("user",)
    list_filter = ("user", "genre", "release_date")
    search_fields = ("user", "genre__title")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "audio")
    list_display_links = ("user",)


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title")
    list_display_links = ("user",)
    search_fields = ("user", "audios__title")
