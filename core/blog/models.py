from django.urls import reverse
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="post"
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    category = models.ManyToManyField("blog.Category", related_name="cat_post")
    image = models.ImageField(blank=True, null=True, upload_to="posts/")
    body = models.TextField()
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.id, "slug": self.slug})

    def __str__(self):
        return self.title
