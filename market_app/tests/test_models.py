from django.test import TestCase
from market_app.models import Market, Seller, Product


class MarketModelTestCase(TestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )

    def test_market_creation(self):
        self.assertEqual(self.market.name, "Downtown Market")
        self.assertEqual(self.market.location, "Munich, Germany")
        self.assertEqual(self.market.description, "A popular market in the city center.")
        self.assertEqual(str(self.market), "Downtown Market")


class SellerModelTestCase(TestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.seller = Seller.objects.create(
            name="John Doe",
            contact_info="john.doe@example.com, +49 123 456 789",
        )
        self.seller.markets.add(self.market)

    def test_seller_creation(self):
        self.assertEqual(self.seller.name, "John Doe")
        self.assertEqual(self.seller.contact_info, "john.doe@example.com, +49 123 456 789")
        self.assertIn(self.market, self.seller.markets.all())
        self.assertEqual(str(self.seller), "John Doe")

    def test_seller_without_markets(self):
        seller = Seller.objects.create(
            name="No Market Seller",
            contact_info="no.market@example.com",
        )
        self.assertEqual(seller.markets.count(), 0)


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.seller = Seller.objects.create(
            name="John Doe",
            contact_info="john.doe@example.com, +49 123 456 789",
        )
        self.seller.markets.add(self.market)
        self.product = Product.objects.create(
            name="Organic Apples",
            description="Fresh organic apples from local farms.",
            price=3.50,
            seller=self.seller,
        )
        self.product.markets.add(self.market)

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Organic Apples")
        self.assertEqual(self.product.description, "Fresh organic apples from local farms.")
        self.assertEqual(self.product.price, 3.50)
        self.assertEqual(self.product.seller, self.seller)
        self.assertIn(self.market, self.product.markets.all())
        self.assertEqual(str(self.product), "Organic Apples (3.50)")

    def test_product_without_markets(self):
        product = Product.objects.create(
            name="Standalone Product",
            description="This product has no markets.",
            price=10.00,
            seller=self.seller,
        )
        self.assertEqual(product.markets.count(), 0)
