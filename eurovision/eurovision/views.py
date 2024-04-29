from django.http import JsonResponse
from .models import Country, Voter, Vote, Song, Contestant
from .serializers import CountrySerializer, VoterSerializer, VoteSerializer, SongSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

#endpoint for the list of countries, artist names and song titles
@api_view(['GET'])
def country_list(request):
    countries = Country.objects.all()
    contestants = Contestant.objects.all()
    songs = Song.objects.all()
    country_list = [country.country_name for country in countries]
    artist_list = [contestant.artist for contestant in contestants]
    song_list = [song.title for song in songs]
    return JsonResponse({"countries": country_list, "artists": artist_list, "songs": song_list}, safe=False)

@api_view(['GET'])
def country_detail(request, country_name):
    country = Country.objects.get(country_name=country_name)
    serializer = CountrySerializer(country, many=False)
    return Response(serializer.data)
#TODO: implement the rest of the details including contestants

@api_view(['GET'])
def song_list(request):
    songs = Song.objects.all()
    title = [song.title for song in songs]
    return JsonResponse(title, safe=False)
    
@api_view(['GET'])
def song_detail(request, title):
    song = Song.objects.get(title=title)
    serializer = SongSerializer(song, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def voter_list(request):
    voters = Voter.objects.all()
    serializer = VoterSerializer(voters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def vote_list(request, username):
    votes = Vote.objects.filter(voter__username=username)
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def vote_detail(request, username, song):
    voter = Voter.objects.filter(username=username).first()
    if not voter:
        return Response({"detail": "Voter not found."}, status=404)
    
    vote = Vote.objects.filter(voter=voter, song__title=song).first()
    if not vote:
        return Response({"detail": "Vote not found."}, status=404)

    serializer = VoteSerializer(vote, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)