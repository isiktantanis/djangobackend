from rest_framework import serializers

from .models import NFT, NFTCollection, NFTCollectionCategory, User, UserFavoritedNFT, UserWatchListedNFTCollection
from djoser.serializers import UserCreateSerializer

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = "__all__"

class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = [
            "UID",
            "index",
            "name",
            "description",
            "metaDataType",
            "dataLink",
            "collectionName",
            "creator",
            "currentOwner",
            "marketStatus",
            "nftFile"
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class NFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollection
        fields = ["name", "description", "owner", "category", "collectionImage"]

class NFTCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollectionCategory
        fields = ["name"]

class UserFavoritedNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritedNFT
        fields = "__all__"

class UserWatchListedNFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchListedNFTCollection
        fields = "__all__"
