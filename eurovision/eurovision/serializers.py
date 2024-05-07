from rest_framework import serializers
from .models import Country, Contestant, Song, Vote, Voter

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name', 'euro_flag_url', 'final_order']

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['country', 'artist', 'about']

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['contestant', 'title', 'yt_video_url', 'lyrics_original', 'lyrics_translated']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['voter', 'country', 'song_quality', 'stage_presence', 'vocal_performance']

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['username', 'first_name', 'last_name']

class CountryScoreSerializer(serializers.Serializer):
    country_name = serializers.CharField()
    final_score = serializers.FloatField()