from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import (
    NFT,
    NFTCollection,
    NFTCollectionCategory,
    User,
    UserFavoritedNFT,
    UserWatchListedNFTCollection,
)


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = "__all__"


class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class NFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollection
        fields = "__all__"


class NFTCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollectionCategory
        fields = "__all__"


class UserFavoritedNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritedNFT
        fields = "__all__"


class UserWatchListedNFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchListedNFTCollection
        fields = "__all__"
