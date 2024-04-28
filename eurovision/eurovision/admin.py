from django.contrib import admin
from .models import Country, Voter, Contestant, Song

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