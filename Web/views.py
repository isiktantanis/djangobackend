from asyncio.windows_events import NULL
from itertools import chain
from tkinter.messagebox import QUESTION
from unicodedata import name
from urllib import request

from django.shortcuts import render
from rest_framework import generics

from .models import NFT, NFTCollection, NFTCollectionCategory, User
from .serializers import (
    NFTCategorySerializer,
    NFTCollectionSerializer,
    NFTSerializer,
    UserSerializer,
)


class NFTListView(generics.ListAPIView):
    def get_queryset(self):
        if self.request.method == "GET":
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
