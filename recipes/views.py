from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from utils.recipes.factory import make_recipe
from .models import Recipe, Category
import pdb
from django.http import HttpResponse

# Create your views here.
def home(request):
    recipe = Recipe.objects.filter(is_published = True).order_by('-id')
    
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
    pdb.set_trace()
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
    else:
        recipe = Recipe()
        recipe.id = id
    return render(request,'recipes/pages/recipe-view.html', context={
        'recipe':recipe,
        'is_detail_page': True,
    })
