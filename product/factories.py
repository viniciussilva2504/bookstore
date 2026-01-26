import factory

from product.models.product import Product
from product.models.category import Category

class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=200)

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=500)
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    active = factory.Iterator([True, False])

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)

    class Meta:
        model = Product