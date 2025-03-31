from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = "__all__"

    def validate_net_worth(self, value):
        if value < 0:
            raise serializers.ValidationError("Net worth cannot be negative.")
        return value


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    markets_ids = serializers.PrimaryKeyRelatedField(
        source="markets", queryset=Market.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Seller
        fields = ["id", "name", "contact_info", "markets", "markets_ids"]


class ProductSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    markets_ids = serializers.PrimaryKeyRelatedField(
        source="markets", queryset=Market.objects.all(), many=True, write_only=True
    )
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(source="seller", queryset=Seller.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "markets", "markets_ids", "seller", "seller_id"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
