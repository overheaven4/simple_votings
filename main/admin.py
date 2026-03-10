from django.contrib import admin
from django.utils.html import format_html
from .models import Voting, VotingOption, Vote

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'created_at', 'options_count')
    list_filter = ('created_at', 'creator')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def options_count(self, obj):
        # Подсчет количества вариантов для конкретного голосования
        return obj.votingoption_set.count()
    options_count.short_description = 'Количество вариантов'

@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'voting', 'text', 'votes_count')
    search_fields = ('text', 'voting__title')
    list_filter = ('voting',)

    def votes_count(self, obj):
        # Подсчет отданных голосов за вариант
        return obj.vote_set.count()
    votes_count.short_description = 'Количество голосов'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'option', 'created_at')
    list_filter = ('created_at', 'option__voting')
    search_fields = ('user__username', 'option__text')
    date_hierarchy = 'created_at'