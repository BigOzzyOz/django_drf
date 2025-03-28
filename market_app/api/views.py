from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(["GET", "POST"])
def first_view(request):
    if request.method == "GET":
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        try:
            data = request.data["message"]
            return Response({"your_data": data}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
