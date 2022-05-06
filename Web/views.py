from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    NFT,
    NFTCollection,
    NFTCollectionCategory,
    TransHist,
    User,
    UserFavoritedNFT,
    UserWatchListedNFTCollection,
)
from .serializers import (
    NFTCategorySerializer,
    NFTCollectionSerializer,
    NFTSerializer,
    TransHistSerializer,
    UserFavoritedNFTSerializer,
    UserSerializer,
    UserWatchListedNFTCollectionSerializer,
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
        NFTToChange = NFT.objects.all().filter(UID=reqData["UID"], index=reqData["index"])
        NFTToChange.update(**reqData)
        if len(NFTToChange) == 0:
            return Response(status=400)
        return Response(status=200)
    # attributes


# TODO: Create Total Likes For NFTCollections


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
        # queryset.delete()
        for user in queryset:
            user.is_active = False
            user.profilePicture = None
            user.save()
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


@api_view(["GET", "POST", "DELETE"])
def UserFavoritedNFTListView(request):
    if request.method == "GET":
        # resolve primary key issue of NFT
        if "nft" not in request.data.keys():
            req = {}
            if "user" in request.data.keys():
                req["user"] = request.data["user"]
            if "UID" in request.data.keys() and "index" in request.data.keys():
                req["nft"] = NFT.objects.all().filter(UID=request.data["UID"], index=request.data["index"])[0].id
            favoriteItems = UserFavoritedNFT.objects.all().filter(**req)
        else:
            favoriteItems = UserFavoritedNFT.objects.all().filter(**request.data)

        # give the client exactly what they want
        # TODO: WRITE SOMETHING SMARTER here
        if "user" in request.data.keys() and not ("nft" in request.data.keys() or "nft" in req.keys()):
            queryset = favoriteItems.values_list("nft", flat=True)
            nfts = NFT.objects.none()
            for ID in queryset:
                nfts = nfts.union(NFT.objects.filter(pk=ID))
            nfts = NFTSerializer(nfts, many=True)
            return Response(nfts.data)
        elif "user" not in request.data.keys() and ("nft" in request.data.keys() or "nft" in req.keys()):
            queryset = favoriteItems.values_list("user", flat=True)
            users = User.objects.none()
            for uAddress in queryset:
                users = users.union(User.objects.filter(uAddress=uAddress))
            users = UserSerializer(users, many=True)
            return Response(users.data)
        else:
            favoriteItems = UserFavoritedNFTSerializer(favoriteItems, many=True)
            return Response(favoriteItems.data)

    elif request.method == "POST":
        # resolve primary key issue of NFT
        if "nft" not in request.data.keys():
            req = {}
            if "user" in request.data.keys():
                req["user"] = request.data["user"]
            if "UID" in request.data.keys() and "index" in request.data.keys():
                req["nft"] = NFT.objects.all().filter(UID=request.data["UID"], index=request.data["index"])[0].id
            newLike = UserFavoritedNFTSerializer(data=req)
        else:
            newLike = UserFavoritedNFTSerializer(data=request.data)

        newLike.is_valid(raise_exception=True)
        newLike.save()
        return Response(newLike.data, status=201)

    elif request.method == "DELETE":
        # resolve primary key issue of NFT
        if "nft" not in request.data.keys():
            req = {}
            if "user" in request.data.keys():
                req["user"] = request.data["user"]
            if "UID" in request.data.keys() and "index" in request.data.keys():
                req["nft"] = NFT.objects.all().filter(UID=request.data["UID"], index=request.data["index"])[0].id
            queryset = UserFavoritedNFT.objects.all().filter(**req)
        else:
            queryset = UserFavoritedNFT.objects.all().filter(**request.data)

        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)


@api_view(["GET", "POST", "DELETE"])
def UserWatchListedNFTCollectionListView(request):
    if request.method == "GET":
        watchListItems = UserWatchListedNFTCollection.objects.all().filter(**request.data)
        if "user" in request.data.keys() and "nftCollection" not in request.data.keys():
            queryset = watchListItems.values_list("nftCollection", flat=True)
            nftCollections = NFTCollection.objects.none()
            for name in queryset:
                nftCollections = nftCollections.union(NFTCollection.objects.filter(name=name))
            nftCollections = NFTCollectionSerializer(nftCollections, many=True)
            return Response(nftCollections.data)
        elif "user" not in request.data.keys() and "nftCollection" in request.data.keys():
            queryset = watchListItems.values_list("user", flat=True)
            users = User.objects.none()
            for uAddress in queryset:
                users = users.union(User.objects.filter(uAddress=uAddress))
            users = UserSerializer(users, many=True)
            return Response(users.data)
        else:
            queryset = UserWatchListedNFTCollectionSerializer(watchListItems, many=True)
            return Response(queryset.data)

    elif request.method == "POST":
        newLike = UserWatchListedNFTCollectionSerializer(data=request.data)
        newLike.is_valid(raise_exception=True)
        newLike.save()
        return Response(newLike.data, status=201)

    elif request.method == "DELETE":
        queryset = UserWatchListedNFTCollection.objects.all().filter(**request.data.dict())
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)


@api_view(["GET", "POST", "DELETE"])
def TransHistListView(request):
    if request.method == "GET":
        queryset = TransHist.objects.all().filter(**request.data)
        queryset = TransHist(queryset, many=True)
        return Response(queryset.data)
    elif request.method == "POST":
        newTransHistObject = TransHistSerializer(data=request.data)
        newTransHistObject.is_valid(raise_exception=True)
        newTransHistObject.save()
        return Response(newTransHistObject.data)
    elif request.method == "DELETE":
        queryset = TransHist.objects.all().filter(**request.data.dict())
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)
