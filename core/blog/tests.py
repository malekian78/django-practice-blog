import pytest
from django.contrib.auth import get_user_model
from .models import Post, Category
from accounts.models.profile import Profile

User = get_user_model()


@pytest.fixture
def user_profile():
    user = User.objects.create_user(email="admin@admin.com", password="a@>/123456")
    profile = Profile.objects.get(user=user)
    return profile


@pytest.fixture
def category():
    category = Category.objects.create(name="CAT1")
    return category

@pytest.mark.django_db
def test_post_create(user_profile, category):
    post = Post.objects.create(
        author=user_profile,
        title="sample_title",
        image=None,
        body="teh body ... ",
        published_date=None,
    )
    post.category.add(category)
    assert post.status == False
    assert post.author.user.email == "admin@admin.com"

