from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

# Create your models here.


User = get_user_model()


class Post(models.Model):
    """
    Post model that create Post table for blog app
    it can be extended to get proper information to api serializer
    """

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to="blog/")
    content = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def get_absolute_api_url(self):
        return reverse_lazy("blog:api-v1:post-detail", kwargs={"pk": self.pk})

    def _get_user_email(self):  # i am wondering this was possible this whole time 😭
        return self.author.user.email

    def __str__(self):
        return self.title


class Category(models.Model):

    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
