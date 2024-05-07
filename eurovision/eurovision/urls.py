from django.contrib import admin
from django.urls import path, include
from eurovision import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    path('countries/', views.country_list),
    path('countries/<str:country_name>/', views.country_detail),
    # path('songs/<str:title>/', views.song_detail),
    # all votes of the user
    # path('results/', views.results),
    path('votes/<str:username>/', views.vote_list),
    # here you can PUT a vote
    # everything else is just a GET
    path('votes/<str:username>/<str:country>/', views.vote_detail),
    # take username from here
    path('voters/', views.voter_list),
    path('results/', views.results),
    path('results/song-quality', views.song_quality),
    path('results/stage-presence', views.stage_presence),
    path('results/vocal-performance', views.vocal_performance),
]
