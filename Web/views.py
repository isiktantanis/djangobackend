from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import NFT, NFTCollection, NFTCollectionCategory, User
from .serializers import (
    NFTCategorySerializer,
    NFTCollectionSerializer,
    NFTSerializer,
    UserSerializer,
)

# TODO: [NFTMAR-145] Enable Cascading on Foreign Keys On "Patch" Requests

@api_view(["GET", "POST", "PATCH", "DELETE"])
def NFTListView(request):

    if request.method == "GET":
        queryset = NFT.objects.all().filter(**request.data)
        queryset = NFTSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newNFTObject = NFTSerializer(data=request.data)
        newNFTObject.is_valid(raise_exception=True)
        newNFTObject.save()
        return Response(newNFTObject.data)

    elif request.method == "DELETE":
        queryset = NFT.objects.all().filter(**request.data.dict())
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)

    elif request.method == "PATCH":
        reqData = request.data.dict()
        NFTToChange = NFT.objects.all().filter(uid=reqData["uid"], nID=reqData["nID"])
        NFTToChange.update(**reqData)
        if len(NFTToChange) == 0:
            return Response(status=400)
        return Response(status=200)
    # attributes


@api_view(["GET", "POST", "PATCH", "DELETE"])
def NFTCollectionListView(request):
    if request.method == "GET":
        queryset = NFTCollection.objects.all().filter(**request.data)
        queryset = NFTCollectionSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newNFTCollectionObject = NFTCollectionSerializer(data=request.data)
        newNFTCollectionObject.is_valid(raise_exception=True)
        newNFTCollectionObject.save()
        return Response(newNFTCollectionObject.data)

    elif request.method == "DELETE":
        queryset = NFTCollection.objects.all().filter(**request.data.dict())
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)

    elif request.method == "PATCH":
        reqData = request.data.dict()
        NFTCollectionToChange = NFTCollection.objects.all().filter(name=reqData["name"])
        NFTCollectionToChange.update(**reqData)
        if len(NFTCollectionToChange) == 0:
            return Response(status=400)
        return Response(status=200)


@api_view(["GET", "POST", "PATCH", "DELETE"])
def UserListView(request):
    if request.method == "GET":
        queryset = User.objects.all().filter(**request.data)
        queryset = UserSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newUserObject = UserSerializer(data=request.data)
        newUserObject.is_valid(raise_exception=True)
        newUserObject.save()
        return Response(newUserObject.data)

    elif request.method == "DELETE":
        queryset = User.objects.all().filter(**request.data.dict())
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)
    # uAdress cannot change.
    elif request.method == "PATCH":
        reqData = request.data.dict()
        UserToChange = User.objects.all().filter(uAddress=reqData["uAddress"])
        UserToChange.update(**reqData)
        if len(UserToChange) == 0:
            return Response(status=400)
        return Response(status=200)


@api_view(["GET", "POST", "PATCH", "DELETE"])
def CategoryListView(request):
    if request.method == "GET":
        queryset = NFTCollectionCategory.objects.all().filter(**request.data)
        queryset = NFTCategorySerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newCategoryObject = NFTCategorySerializer(data=request.data)
        newCategoryObject.is_valid(raise_exception=True)
        newCategoryObject.save()
        return Response(newCategoryObject.data)

    elif request.method == "DELETE":
        queryset = NFTCollectionCategory.objects.all().filter(**request.data.dict())
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)

    elif request.method == "PATCH":
        reqData = request.data.dict()
        NFTCategoryToChange = NFTCollectionCategory.objects.all().filter(name=reqData["pk"])
        if len(NFTCategoryToChange) == 0:
            return Response(status=400)
        NFTCategoryToChange.update(name=reqData["name"])
        return Response(status=200)


# Create your views here.
