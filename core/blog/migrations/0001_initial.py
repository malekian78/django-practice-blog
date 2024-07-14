# Generated by Django 4.2 on 2024-07-14 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=250)),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("slug", models.SlugField(unique=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="posts/")),
                ("body", models.TextField()),
                ("status", models.BooleanField(default=False)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("published_date", models.DateTimeField(blank=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post",
                        to="accounts.profile",
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(related_name="cat_post", to="blog.category"),
                ),
            ],
        ),
    ]
