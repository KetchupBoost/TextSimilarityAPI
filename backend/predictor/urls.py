from django.urls import path
from .views import pdf

urlpatterns = [
    path('', pdf, name='PDF')
]
