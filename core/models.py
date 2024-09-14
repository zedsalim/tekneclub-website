from django.db import models
from django.utils.text import slugify
from users.models import *

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=254, unique=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_base = slugify(self.name)
            slug = slug_base
            num = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{num}"
                num += 1
            
            self.slug = slug
        else:
            existing_category = Category.objects.get(pk=self.pk)
            new_slug = slugify(self.name)
            
            if existing_category.name != self.name:
                slug_base = new_slug
                slug = slug_base
                num = 1

                while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{slug_base}-{num}"
                    num += 1
                
                self.slug = slug
            else:
                self.slug = existing_category.slug
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS = (
        ("Draft", "Draft"),
        ("Published", "Published"),
        ("Archived", "Archived"),
    )
    TYPE = (
        ("Blog", "Blog"),
        ("Event", "Event"),
    )
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    slug = models.SlugField(max_length=254, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Draft")
    post_type = models.CharField(max_length=20, choices=TYPE, default="Blog")
    categories = models.ManyToManyField(Category, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_base = slugify(self.title)
            slug = slug_base
            num = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{num}"
                num += 1
            
            self.slug = slug
        else:
            existing_post = Post.objects.get(pk=self.pk)
            new_slug = slugify(self.title)
            
            if existing_post.title != self.title:
                slug_base = new_slug
                slug = slug_base
                num = 1

                while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{slug_base}-{num}"
                    num += 1
                
                self.slug = slug
            else:
                self.slug = existing_post.slug
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'Post: {self.title}'


class PostImages(models.Model):
    image = models.ImageField(upload_to="images/")
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Post Images"

    def __str__(self):
        if self.post:
            return f"Image for: {self.post.title}"
        else:
            return f"Orphaned Image"