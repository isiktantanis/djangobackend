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
        fields = ['uAddress', 'last_login', 'username', 'profilePicture', 'email', 'is_active', 'is_superuser',
                  'is_staff', 'date_joined']


class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = ['id', 'UID', 'index', 'name', 'description', 'metaDataType', 'dataLink', 'marketStatus', 'nftFile',
                  'numLikes', 'collectionName', 'creator', 'currentOwner']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uAddress', 'last_login', 'username', 'profilePicture', 'email', 'is_active', 'is_superuser',
                  'is_staff', 'date_joined']



class NFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollection
        fields = ['name', 'collectionImage', 'description', 'numLikes', 'owner', 'category']


class NFTCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollectionCategory
        fields = ["name"]


class UserFavoritedNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritedNFT
        fields = ["nft", "user"]


class UserWatchListedNFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchListedNFTCollection
        fields = ["nftCollection", "user"]
