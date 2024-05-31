from django.urls import path #re_path caso queria usar expressões regulares (pesquisar)
from .views import * #from . import views

app_name = 'recipes'

urlpatterns = [
    path('', RecipeListViewBase.as_view(), name="home"),
    path('recipes/category/<int:category_id>/', RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:id>/', RecipeDetail.as_view(), name="recipe"),
    path('recipes/search/', RecipeListViewSearch.as_view(), name="search"),
]
