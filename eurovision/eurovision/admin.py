from django.contrib import admin
from .models import Country, Voter, Contestant, Song, Vote

admin.site.register(Country)
admin.site.register(Contestant)
admin.site.register(Song)

class VoterAdminForm(admin.ModelAdmin):
    model = Voter
    fields = ['first_name', 'last_name']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.save()

admin.site.register(Voter, VoterAdminForm)

def reset_votes(modeladmin, request, queryset):
    queryset.update(song_quality=None, stage_presence=None, vocal_performance=None)
reset_votes.short_description = "Reset Votes"

class VoteAdmin(admin.ModelAdmin):
    actions = [reset_votes]

admin.site.register(Vote, VoteAdmin)