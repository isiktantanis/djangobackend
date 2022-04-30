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


class NFTCollectionListView(generics.ListAPIView):
    def get_queryset(self):
        name = self.request.query_params.get("name")
        owner = self.request.query_params.get("owner")
        category = self.request.query_params.get("category")
        queryset = NFTCollection.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        if owner:
            queryset = queryset.filter(owner=owner)
        if category:
            queryset = queryset.filter(category=category)
        print("woop:", queryset.filter(NFT__pk=1))
        return queryset

    serializer_class = NFTCollectionSerializer


class UserListView(generics.ListAPIView):
    def get_queryset(self):
        uAdress = self.request.query_params.get("address")
        username = self.request.query_params.get("username")
        mailAdress = self.request.query_params.get("email")
        queryset = User.objects.all()
        if username:
            queryset = queryset.filter(username__icontains=username)
        if uAdress:
            queryset = queryset.filter(uAdress=uAdress)
        if mailAdress:
            queryset = queryset.filter(mailAdress=mailAdress)
        return queryset

    serializer_class = UserSerializer


class CategoryListView(generics.ListAPIView):
    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = NFTCollectionCategory.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    serializer_class = NFTCategorySerializer


# Create your views here.
