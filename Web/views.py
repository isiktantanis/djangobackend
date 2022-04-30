from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from .models import NFT, NFTCollection, NFTCollectionCategory, User
from .serializers import (
    NFTCategorySerializer,
    NFTCollectionSerializer,
    NFTSerializer,
    UserSerializer,
)
from rest_framework.decorators import api_view


@api_view(["GET", "POST", "PATCH", "DELETE"])
def NFTListView(request):

    if request.method == "GET":
        queryset = NFT.objects.all().filter(**request.data)
        queryset = NFTSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newNFTObject = NFTSerializer(data=request.data)
        newNFTObject.is_valid(raise_exception=True)
        newNFTObject.save()
        return Response(newNFTObject.data)

    elif request.method == "DELETE":
        queryset = NFT.objects.all().filter(**request.data.dict())
        queryset.delete()
        return Response(status=200)
    # attributes

@api_view(["GET", "POST", "PATCH", "DELETE"])
def NFTCollectionListView(request):
    if request.method == "GET":
        queryset = NFTCollection.objects.all().filter(**request.data)
        queryset = NFTCollectionSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newNFTCollectionObject = NFTCollectionSerializer(data=request.data)
        newNFTCollectionObject.is_valid(raise_exception=True)
        newNFTCollectionObject.save()
        return Response(newNFTCollectionObject.data)

    elif request.method == "DELETE":
        queryset = NFTCollection.objects.all().filter(**request.data.dict())
        queryset.delete()
        return Response(status=200)

@api_view(["GET", "POST", "PATCH", "DELETE"])
def UserListView(request):
    if request.method == "GET":
        queryset = User.objects.all().filter(**request.data)
        queryset = UserSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newUserObject = UserSerializer(data=request.data)
        newUserObject.is_valid(raise_exception=True)
        newUserObject.save()
        return Response(newUserObject.data)

    elif request.method == "DELETE":
        queryset = User.objects.all().filter(**request.data.dict())
        queryset.delete()
        return Response(status=200)


@api_view(["GET", "POST", "PATCH", "DELETE"])
def CategoryListView(request):
    if request.method == "GET":
        queryset = NFTCollectionCategory.objects.all().filter(**request.data)
        queryset = NFTCategorySerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newCategoryObject = NFTCategorySerializer(data=request.data)
        newCategoryObject.is_valid(raise_exception=True)
        newCategoryObject.save()
        return Response(newCategoryObject.data)

    elif request.method == "DELETE":
        queryset = NFTCollectionCategory.objects.all().filter(**request.data.dict())
        queryset.delete()
        return Response(status=200)



# Create your views here.
