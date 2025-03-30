from django.test import TestCase
from market_app.models import Market, Seller
from market_app.api.serializers import MarketSerializer, SellerCreateSerializer, ProductCreateSerializer


class MarketSerializerTestCase(TestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.serializer = MarketSerializer(instance=self.market)

    def test_market_serialization(self):
        data = self.serializer.data
        self.assertEqual(data["name"], "Downtown Market")
        self.assertEqual(data["location"], "Munich, Germany")
        self.assertEqual(data["description"], "A popular market in the city center.")
        self.assertEqual(data["net_worth"], "1200000.50")

    def test_invalid_market_serialization(self):
        data = {
            "name": "",
            "location": "Munich, Germany",
            "description": "A market with no name.",
            "net_worth": "100000.00",
        }
        serializer = MarketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_market_net_worth_negative(self):
        data = {
            "name": "Invalid Market",
            "location": "Nowhere",
            "description": "This should fail.",
            "net_worth": "-1000.00",
        }
        serializer = MarketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("net_worth", serializer.errors)


class SellerCreateSerializerTestCase(TestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.data = {
            "name": "John Doe",
            "contact_info": "john.doe@example.com, +49 123 456 789",
            "markets": [self.market.id],
        }
        self.serializer = SellerCreateSerializer(data=self.data)

    def test_seller_serialization(self):
        self.assertTrue(self.serializer.is_valid())
        seller = self.serializer.save()
        self.assertEqual(seller.name, "John Doe")
        self.assertEqual(seller.contact_info, "john.doe@example.com, +49 123 456 789")
        self.assertIn(self.market, seller.markets.all())

    def test_invalid_seller_serialization(self):
        data = {
            "name": "",
            "contact_info": "invalid@example.com",
            "markets": [],
        }
        serializer = SellerCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class ProductCreateSerializerTestCase(TestCase):
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
        self.data = {
            "name": "Organic Apples",
            "description": "Fresh organic apples from local farms.",
            "price": 3.50,
            "markets": [self.market.id],
            "seller": self.seller.id,
        }
        self.serializer = ProductCreateSerializer(data=self.data)

    def test_product_serialization(self):
        self.assertTrue(self.serializer.is_valid())
        product = self.serializer.save()
        self.assertEqual(product.name, "Organic Apples")
        self.assertEqual(product.description, "Fresh organic apples from local farms.")
        self.assertEqual(product.price, 3.50)
        self.assertEqual(product.seller, self.seller)
        self.assertIn(self.market, product.markets.all())

    def test_invalid_product_description(self):
        data = {
            "name": "Invalid Product",
            "description": "",
            "price": 10.00,
            "markets": [self.market.id],
            "seller": self.seller.id,
        }
        serializer = ProductCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_invalid_product_price(self):
        data = {
            "name": "Invalid Product",
            "description": "Valid description",
            "price": -10.00,
            "markets": [self.market.id],
            "seller": self.seller.id,
        }
        serializer = ProductCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)
