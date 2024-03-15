from django.contrib import admin
from django.urls import path, include
from eurovision import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('countries/', views.country_list),
    path('api-auth/', include('rest_framework.urls'))
]
