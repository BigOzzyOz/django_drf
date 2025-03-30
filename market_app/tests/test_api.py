from rest_framework.test import APITestCase
from rest_framework import status
from market_app.models import Market, Seller, Product


class MarketAPITestCase(APITestCase):
    def setUp(self):
        self.market1 = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.market2 = Market.objects.create(
            name="Green Valley Market",
            location="Hamburg, Germany",
            description="Known for its organic and eco-friendly products.",
            net_worth="750000.75",
        )

    def test_get_markets(self):
        response = self.client.get("/api/markets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_market_detail(self):
        response = self.client.get(f"/api/markets/{self.market1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Downtown Market")

    def test_create_market(self):
        data = {
            "name": "Central Market",
            "location": "Berlin, Germany",
            "description": "A large market with a variety of goods and services.",
            "net_worth": "5000000.00",
        }
        response = self.client.post("/api/markets/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Central Market")

    def test_update_market(self):
        data = {
            "name": "Updated Market",
            "location": "Munich, Germany",
            "description": "Updated description.",
            "net_worth": "1500000.00",
        }
        response = self.client.put(f"/api/markets/{self.market1.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Market")

    def test_delete_market(self):
        response = self.client.delete(f"/api/markets/{self.market1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Market.objects.filter(id=self.market1.id).exists())


class SellerAPITestCase(APITestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.seller = Seller.objects.create(name="John Doe", contact_info="john.doe@example.com, +49 123 456 789")
        self.seller.markets.add(self.market)

    def test_get_sellers(self):
        response = self.client.get("/api/sellers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_seller_detail(self):
        response = self.client.get(f"/api/sellers/{self.seller.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")

    def test_create_seller(self):
        data = {
            "name": "Jane Smith",
            "contact_info": "jane.smith@example.com, +49 987 654 321",
            "markets": [self.market.id],
        }
        response = self.client.post("/api/sellers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Jane Smith")

    def test_update_seller(self):
        data = {"name": "Updated Seller", "contact_info": "updated@example.com", "markets": [self.market.id]}
        response = self.client.put(f"/api/sellers/{self.seller.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Seller")

    def test_delete_seller(self):
        response = self.client.delete(f"/api/sellers/{self.seller.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Seller.objects.filter(id=self.seller.id).exists())


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.market = Market.objects.create(
            name="Downtown Market",
            location="Munich, Germany",
            description="A popular market in the city center.",
            net_worth="1200000.50",
        )
        self.seller = Seller.objects.create(name="John Doe", contact_info="john.doe@example.com, +49 123 456 789")
        self.seller.markets.add(self.market)
        self.product = Product.objects.create(
            name="Organic Apples",
            description="Fresh organic apples from local farms.",
            price="3.50",
            seller=self.seller,
        )
        self.product.markets.add(self.market)

    def test_get_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Organic Apples")

    def test_create_product(self):
        data = {
            "name": "Handmade Baskets",
            "description": "Beautiful handmade baskets for daily use.",
            "price": "15.00",
            "markets": [self.market.id],
            "seller": self.seller.id,
        }
        response = self.client.post("/api/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Handmade Baskets")

    def test_update_product(self):
        data = {
            "name": "Updated Product",
            "description": "Updated description.",
            "price": "20.00",
            "markets": [self.market.id],
            "seller": self.seller.id,
        }
        response = self.client.put(f"/api/products/{self.product.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Product")

    def test_delete_product(self):
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
