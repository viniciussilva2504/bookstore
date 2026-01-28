import factory
from order.models import Order
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)