from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from .models import Country, Voter, Vote
from .serializers import CountrySerializer, VoterSerializer, VoteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def country_list(request):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def country_detail(request, pk):
    country = Country.objects.get(code=pk)
    serializer = CountrySerializer(country, many=False)
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