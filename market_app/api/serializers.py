from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.location = validated_data.get("location", instance.location)
        instance.description = validated_data.get("description", instance.description)
        instance.net_worth = validated_data.get("net_worth", instance.net_worth)
        instance.save()
        return instance

    def validate_net_worth(self, value):
        if value < 0:
            raise serializers.ValidationError("Net worth cannot be negative.")
        return value


class SellerReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def create(self, validated_data):
        markets_data = validated_data.pop("markets")
        seller = Seller.objects.create(**validated_data)
        for market_id in markets_data:
            try:
                market = Market.objects.get(id=market_id)
                seller.markets.add(market)
            except Market.DoesNotExist:
                raise serializers.ValidationError(f"Market with id {market_id} does not exist.")
        return seller

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.contact_info = validated_data.get("contact_info", instance.contact_info)
        markets_data = validated_data.get("markets", [])
        instance.markets.clear()
        for market_id in markets_data:
            try:
                market = Market.objects.get(id=market_id)
                instance.markets.add(market)
            except Market.DoesNotExist:
                raise serializers.ValidationError(f"Market with id {market_id} does not exist.")
        instance.save()
        return instance

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("Some markets do not exist.")
        return value


class ProductReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    markets = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    seller = serializers.PrimaryKeyRelatedField(read_only=True)


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True)

    def create(self, validated_data):
        markets_data = validated_data.pop("markets")
        product = Product.objects.create(**validated_data)
        for market_id in markets_data:
            try:
                market = Market.objects.get(id=market_id)
                product.markets.add(market)
            except Market.DoesNotExist:
                raise serializers.ValidationError(f"Market with id {market_id} does not exist.")
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.seller = validated_data.get("seller", instance.seller)
        markets_data = validated_data.get("markets", [])
        instance.markets.clear()
        for market_id in markets_data:
            try:
                market = Market.objects.get(id=market_id)
                instance.markets.add(market)
            except Market.DoesNotExist:
                raise serializers.ValidationError(f"Market with id {market_id} does not exist.")
        instance.save()
        return instance

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
