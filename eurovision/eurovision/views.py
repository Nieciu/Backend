from django.http import JsonResponse
from .models import Country, Voter, Vote, Song
from .serializers import CountrySerializer, VoterSerializer, VoteSerializer, SongSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def country_list(request):
    songs = Song.objects.all()
    data = []
    for song in songs:
        data.append({
            'country': song.contestant.country.country_name,
            'artist': song.contestant.artist,
            'song': song.title
        })
    return JsonResponse(data, safe=False)

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
def vote_detail(request, username, country):
    voter = Voter.objects.filter(username=username).first()
    if not voter:
        return Response({"detail": "Voter not found."}, status=404)
    
    vote = Vote.objects.filter(voter=voter, country__country_name=country).first()
    if not vote:
        return Response({"detail": "Vote not found."}, status=404)
    data = {**request.data, 'username': username, 'country':country}
    serializer = VoteSerializer(instance=vote, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)