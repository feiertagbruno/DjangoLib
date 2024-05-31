from django.views import View
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(login_url="authors:login", redirect_field_name="next"),name="dispatch")
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def setup(self,*args, **kwargs):
        return super().setup(*args, **kwargs)
    
    def dispatch(self,*args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.get(
                is_published = False,
                author = self.request.user,
                pk = id,
            )
            if not recipe:
                raise Http404
        return recipe

    def render_recipe(self, context):
        return render(self.request, "authors/pages/dashboard_recipe.html", context)

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        
        form = AuthorRecipeForm(
            instance=recipe
        )

        context = {
            "form": form,
        }

        return self.render_recipe(context)

    def post(self, request):
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()
            messages.success(request, "Sua receita foi salva com sucesso.")
            return redirect(reverse("authors:dashboard_recipe_edit", kwargs={"id":recipe.id}))

        context = {
            "form": form,
        }
        return self.render_recipe(context)

@method_decorator(login_required(login_url="authors:login", redirect_field_name="next"),name="dispatch")
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get("recipe_id"))
        recipe.delete()
        messages.success(self.request, "Deleted successfully.")
        return redirect(reverse("authors:dashboard"))