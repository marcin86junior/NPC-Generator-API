from django.contrib import admin
from .models import Story, Character


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'faction', 'profession', 'story', 'created_at')
    search_fields = ('name', 'faction', 'profession')
    list_filter = ('faction', 'profession', 'created_at')
    ordering = ('-created_at',)
