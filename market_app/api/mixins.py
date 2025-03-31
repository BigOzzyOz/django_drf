class MarketCountMixin:
    def get_market_count(self, obj):
        return obj.markets.count()
