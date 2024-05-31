from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=65)
    def __str__(self):
        return str(self.id) + " - " + str(self.name)

class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        #pdb.set_trace()
        return str(self.id) + " - " + str(self.title)

    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"id":self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
        else:
            slug = self.slug
        i = 0
        nova_slug = slug
        while Recipe.objects.filter(slug=nova_slug).exists():
            nova_slug = f"{slug}{i}"
            i += 1
        self.slug = nova_slug
        super().save(*args, **kwargs)