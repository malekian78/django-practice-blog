import pytest
from accounts.models import MyUser

@pytest.mark.django_db
def test_create_user():

    user = MyUser.objects.create_user(
        email="email@email.com", password="eprqp12412sd12"
    )
    assert user != None
    assert user.is_staff == False
    assert user.is_superuser == False

@pytest.mark.django_db
def test_create_superuser():

    user = MyUser.objects.create_superuser(
        email="email@email.com", password="eprqp12412sd12"
    )
    assert user.is_superuser == True