from django.test import TestCase
from warehouse.models import Category


class CategoryModelTests(TestCase):

    def test_category_was_created(self):
        """
        Create new category with `category_name` equals Test980665
        """
        new_category = Category.objects.create(category_name='Test980665')
        self.assertEqual(new_category.category_name, 'Test980665')
