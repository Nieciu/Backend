from django.http import JsonResponse
from .models import Country
from .serializers import CountrySerializer

def country_list(request):

    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return JsonResponse(serializer.data, safe=False)