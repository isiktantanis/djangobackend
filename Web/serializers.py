from rest_framework import serializers

from .models import NFT, NFTCollection, NFTCollectionCategory, User


class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = [
            "uid",
            "nID",
            "name",
            "description",
            "metaDataType",
            "dataLink",
            "collectionName",
            "creatorName",
            "currentOwner",
            "marketStatus",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uAdress",
            "username",
            "profilePicture",
            "mailAdress",
            "password"
            # "favouritedNFTs",
            # "watchListedNFTCollections",
        ]


class NFTCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollection
        fields = ["name", "description", "owner", "category"]


class NFTCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTCollectionCategory
        fields = ["name"]