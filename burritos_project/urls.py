from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def bienvenido(request):
    return HttpResponse("¡Bienvenido a la API de Burritos To Go!")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('', bienvenido, name='bienvenido'),
]