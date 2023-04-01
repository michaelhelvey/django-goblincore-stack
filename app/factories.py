import factory

from app.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.lazy_attribute(
        lambda user: f"{user.first_name.lower()}.{user.last_name.lower()}@email.com"
    )
