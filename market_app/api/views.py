from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import MarketSerializer
from market_app.models import Market


@api_view(["GET", "POST"])
def markets_view(request):
    if request.method == "GET":
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PUT", "DELETE", "PATCH"])
def market_detail_view(request, pk):
    try:
        market = Market.objects.get(pk=pk)
    except Market.DoesNotExist:
        return Response({"error": "Market not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MarketSerializer(market)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        market.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = MarketSerializer(market, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = MarketSerializer(market, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
