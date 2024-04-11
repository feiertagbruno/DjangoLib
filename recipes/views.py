from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from utils.recipes.factory import make_recipe, gen_random_int
from .models import Recipe, Category
import pdb
from django.db.models import Q

# Create your views here.
def home(request):
    recipe = Recipe.objects.filter(is_published = True).order_by('-id')
    if len(recipe) == 0:
        new_obj = Recipe()
        not_found_id = gen_random_int()
        while len(Recipe.objects.filter(id = not_found_id)) != 0:
            not_found_id = gen_random_int()
        new_obj.id = not_found_id
        new_obj.title = "No Recipe Found"
        new_obj.is_published = False
        recipe = [new_obj]
    
    #pdb.set_trace()
    return render(request,'recipes/pages/home.html', context={
        #'recipes':[make_recipe() for _ in range(20)],
        'recipes':recipe,
    })

def category(request, category_id):
    # EXEMPLO ACESSANDO AS INFORMAÇÕES DA TABELA FOREIGNKEYS USANDO DOIS UNDERLINES
    #nm = Category.objects.get(id = category_id).name
    #recipe = Recipe.objects.filter(is_published = True, category__name=nm).order_by('-id')
    #pdb.set_trace()
    recipe = Recipe.objects.filter(is_published=True, category=category_id).order_by('-id')
    #pdb.set_trace()
    # ESSE IF É A VERIFICAÇÃO SE EXISTE O ID DA CATEGORIA DIGITADA NA URL, CASO NÃO EXISTA, RETORNA PAGE VAZIA
    # EU VOU DEIXAR ASSIM, POIS PREFIRO, MAS VOU ANOTAR EM BAIXO EXEMPLOS DA AULA DE COMO RETORNAR 404
    if len(Category.objects.filter(id=category_id)) > 0:
        category = Category.objects.get(id=category_id)
    else:
        category = Category()
        category.name = "Not Found"
    return render(request,'recipes/pages/category.html', context={
        # USADO ANTES DOS TESTES "REAIS" DAS RECEITAS USANDO A BIB FAKER
        #'recipes':[make_recipe() for _ in range(20)],
        'recipes':recipe,
        'category':f"Category - {category.name}",
    })

    #EXEMPLOS DE COMO RETORNAR 404
    #if not recipes:
        #return HttpResponse(content='Not Found', status=404)
        #ou
        #raise Http404('Not Found ')
        #ou


def recipe(request, id):
    if len(Recipe.objects.filter(id=id))>0:
        recipe = Recipe.objects.get(id=id)
        if recipe.is_published != True:
            recipe = Recipe()
            recipe.id = id
            recipe.title = "Recipe Not Published"
    else:
        recipe = Recipe()
        recipe.id = id
        recipe.title = "Not Found"
    return render(request,'recipes/pages/recipe-view.html', context={
        'recipe':recipe,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get("q", "").strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
        Q(title__icontains=search_term) | 
        Q(description__icontains = search_term),
        ),
        is_published = True,
    ).order_by("-id")
        # i antes de contains serve como ignorecase

    return render(request, "recipes/pages/search.html", {
        "page_title": f"Search for '{search_term}'",
        "search_term": search_term,
        "recipes":recipes,
    })