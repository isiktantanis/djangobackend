from django.shortcuts import render
from rest_framework import generics

from .models import NFT, NFTCollection, User
from .serializers import NFTCollectionSerializer, NFTSerializer, UserSerializer


class NFTListView(generics.ListAPIView):
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer


class NFTCollectionListView(generics.ListAPIView):
    queryset = NFTCollection.objects.all()
    serializer_class = NFTCollectionSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Create your views here.
