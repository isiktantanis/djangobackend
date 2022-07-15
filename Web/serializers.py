from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import (
    NFT,
    NFTCollection,
    NFTCollectionCategory,
    TransHist,
    User,
    UserFavoritedNFT,
    UserWatchListedNFTCollection,
)


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            "uAddress",
            "username",
            "profilePicture",
            "email",
            "is_active",
            "date_joined",
            "totalCollectionLikes",
            "totalNFTLikes"
        ]


class UserDeleteSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["password"]


class NFTSerializer(serializers.ModelSerializer):
    collectionName = serializers.CharField(source='collection.name')
    address = serializers.CharField(source='collection.address')

    class Meta:
        model = NFT
        fields = [
            "address",
            "nID",
            "name",
            "description",
            "metaDataType",
            "dataLink",
            "marketStatus",
            "nftFile",
            "numLikes",
            "collectionName",
            "creator",
            "currentOwner",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uAddress",
            "username",
            "profilePicture",
            "email",
            "is_active",
            "date_joined",
            "totalCollectionLikes",
            "totalNFTLikes"
        ]


class NFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollection
        fields = [
            "name",
            "collectionImage",
            "description",
            "numLikes",
            "owner",
            "category",
            "totalNFTLikes",
        ]


class NFTCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollectionCategory
        fields = ["name", "backgroundPicture", "foregroundPicture"]


class UserFavoritedNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritedNFT
        fields = ["nft", "user"]


class UserWatchListedNFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchListedNFTCollection
        fields = ["nftCollection", "user"]


class TransHistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransHist
        fields = ["oldOwner", "newOwner", "price", "time", "nft"]
