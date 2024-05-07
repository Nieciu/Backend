from django.http import JsonResponse
from django.db.models import F, Avg
from .models import Country, Voter, Vote, Song
from .serializers import CountrySerializer, VoterSerializer, VoteSerializer, SongSerializer, CountryScoreSerializer
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
    try:
        voter = Voter.objects.get(username=username)
        country = Country.objects.get(country_name=country)
        vote = Vote.objects.get(voter=voter, country=country)
    except Voter.DoesNotExist:
        return Response({'error': 'Voter not found'}, status=404)
    except Country.DoesNotExist:
        return Response({'error': 'Country not found'}, status=404)
    except Vote.DoesNotExist:
        return Response({'error': 'Vote not found'}, status=404)

    serializer = VoteSerializer(vote, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def results(request):
    countries = Country.objects.filter(
        vote__song_quality__isnull=False, 
        vote__stage_presence__isnull=False, 
        vote__vocal_performance__isnull=False
    ).annotate(
        final_score=Avg(
            (F('vote__song_quality') + F('vote__stage_presence') + F('vote__vocal_performance')) / 3.0
        )
    ).order_by('-final_score')

    serializer = CountryScoreSerializer(countries, many=True)
    return Response(serializer.data)