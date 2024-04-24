from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from .models import Country
from .serializers import CountrySerializer
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

