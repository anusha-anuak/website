from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, Cart, CartItem
from django.contrib.auth.models import User

class StoreTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=10.00,
            stock=5
        )
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_add_to_cart(self):
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Check if cart session created
        session = self.client.session
        self.assertTrue('cart_session' in session)
        
        # Check if item in db
        cart = Cart.objects.get(session_id=session.session_key)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)

    def test_checkout_redirect_if_empty(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('checkout'))
        # Should redirect to product list if cart empty
        self.assertRedirects(response, reverse('product_list'))
