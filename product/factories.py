import factory
from decimal import Decimal

from product.models import Product
from product.models import Category

class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    description = factory.Faker('text')

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.LazyFunction(lambda: Decimal('100.00'))
    title = factory.Faker('word')
    description = factory.Faker('text')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Se extracted é uma lista ou queryset
            if hasattr(extracted, '__iter__') and not isinstance(extracted, (str, Category)):
                for cat in extracted:
                    self.category.add(cat)
            else:
                # Se é uma única categoria
                self.category.add(extracted)

    class Meta:
        model = Product