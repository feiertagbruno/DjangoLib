from django.urls import path #re_path caso queria usar expressões regulares (pesquisar)
from .views import * #from . import views

app_name = 'recipes'

urlpatterns = [
    path('', home, name="home"),
    path('recipes/<int:id>/', recipe, name="recipe")
]
