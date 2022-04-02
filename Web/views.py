from django.shortcuts import render
from rest_framework import generics

from .models import NFT, NFTCollection, User
from .serializers import NFTSerializer


class NFTListView(generics.ListAPIView):
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer


# Create your views here.
