from django.urls import path #re_path caso queria usar expressões regulares (pesquisar)
from .views import * #from . import views

app_name = 'recipes'

urlpatterns = [
    path('', home, name="home"),
    path('recipes/category/<int:category_id>/', category, name="category"),
    path('recipes/<int:id>/', recipe, name="recipe"),
    path('recipes/search/', search, name="search"),
]
