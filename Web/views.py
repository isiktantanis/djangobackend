from asyncio.windows_events import NULL
from urllib import request

from django.shortcuts import render
from rest_framework import generics

from .models import NFT, NFTCollection, User
from .serializers import NFTCollectionSerializer, NFTSerializer, UserSerializer


class NFTListView(generics.ListAPIView):
    def get_queryset(self):
        
        collectionName = self.request.query_params.get("collectionName")
        creatorName = self.request.query_params.get("creatorName")
        uid = self.request.query_params.get("uid")
        nid = self.request.query_params.get("nID")
        queryset = NFT.objects.all()
        if collectionName:
            queryset = queryset.filter(collectionName=collectionName)
        if creatorName:
            queryset = queryset.filter(creatorName=creatorName)
        if uid:
            queryset = queryset.filter(uid=uid)
            if nid:
                queryset = queryset.filter(nID=nid)
        return queryset

    # attributes

    serializer_class = NFTSerializer


class NFTCollectionListView(generics.ListAPIView):
    def get_queryset(self):
        queryset = NFTCollection.objects.all()
        name = self.request.query_params.get("name")
        return super().get_queryset()

    serializer_class = NFTCollectionSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Create your views here.
