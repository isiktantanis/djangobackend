from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from datetime import datetime

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
    def to_representation(self, instance):
        serializedUser = super(UserCreateSerializer, self).to_representation(instance)
        NFTLikes = instance.likes.count()
        collectionLikes = instance.watchLists.count()
        serializedUser.update({"NFTLikes": NFTLikes, "collectionLikes": collectionLikes})
        return serializedUser

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            "uAddress",
            "username",
            "profilePicture",
            "email",
            "is_active",
            "date_joined",
        ]


class UserDeleteSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["password"]


class NFTSerializer(serializers.ModelSerializer):
    collectionName = serializers.CharField(source='collection.name')
    address = serializers.CharField(source='collection.address')

    def to_representation(self, instance):
        serializedNFT = super(NFTSerializer, self).to_representation(instance)
        numLikes = instance.likedBy.count()
        serializedNFT.update({"numLikes": numLikes})
        return serializedNFT

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
            "collectionName",
            "creator",
            "currentOwner",
        ]


class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        serializedNFT = super(UserSerializer, self).to_representation(instance)
        NFTLikes = instance.likes.count()
        collectionLikes = instance.watchLists.count()
        serializedNFT.update({"NFTLikes": NFTLikes, "collectionLikes": collectionLikes})
        return serializedNFT

    class Meta:
        model = User
        fields = [
            "uAddress",
            "username",
            "profilePicture",
            "email",
            "is_active",
            "date_joined",
        ]

class NFTCollectionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serializedCollection = super(NFTCollectionSerializer, self).to_representation(instance)
        numLikes = instance.watchListedBy.count()
        NFTs = instance.nft_list.all()
        NFTLikes = sum([nft.likedBy.count() for nft in NFTs])
        serializedCollection.update({"numLikes": numLikes, "NFTLikes": NFTLikes})
        return serializedCollection

    class Meta:
        model = NFTCollection
        fields = [
            "address",
            "name",
            "collectionImage",
            "description",
            "owner",
            "category",
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