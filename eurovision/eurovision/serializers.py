from rest_framework import serializers
from .models import Country, Contestant, Song

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['code', 'country_name']

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['country', 'artist', 'about']

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['contestant', 'title', 'yt_video_url']