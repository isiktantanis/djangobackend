from datetime import date, datetime

from django.db.models import Count, Max
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
        queryset = NFT.objects.all().filter(**request.GET.dict())
        queryset = NFTSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newNFTObject = NFTSerializer(data=request.data)
        newNFTObject.is_valid(raise_exception=True)
        newNFTObject.save()
        return Response(newNFTObject.data)

    elif request.method == "DELETE":
        queryset = NFT.objects.all().filter(**request.data)
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
        queryset = NFTCollection.objects.all().filter(**request.GET.dict())
        queryset = NFTCollectionSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newNFTCollectionObject = NFTCollectionSerializer(data=request.data)
        newNFTCollectionObject.is_valid(raise_exception=True)
        newNFTCollectionObject.save()
        return Response(newNFTCollectionObject.data)

    elif request.method == "DELETE":
        queryset = NFTCollection.objects.all().filter(**request.data)
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
        queryset = User.objects.all().filter(**request.GET.dict())
        queryset = UserSerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newUserObject = UserSerializer(data=request.data)
        newUserObject.is_valid(raise_exception=True)
        newUserObject.save()
        return Response(newUserObject.data)

    elif request.method == "DELETE":
        queryset = User.objects.all().filter(**request.data)
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
        queryset = NFTCollectionCategory.objects.all().filter(**request.GET.dict())
        queryset = NFTCategorySerializer(queryset, many=True)
        return Response(queryset.data)

    elif request.method == "POST":
        newCategoryObject = NFTCategorySerializer(data=request.data)
        newCategoryObject.is_valid(raise_exception=True)
        newCategoryObject.save()
        return Response(newCategoryObject.data)

    elif request.method == "DELETE":
        queryset = NFTCollectionCategory.objects.all().filter(**request.data)
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
        reqData = request.GET.dict()
        req = {}
        if "user" in reqData.keys():
            req["user"] = reqData["user"]
        if "UID" in reqData.keys() and "index" in reqData.keys():
            req["nft"] = NFT.objects.filter(UID=reqData["UID"], index=reqData["index"])
            if len(req["nft"]) == 0:
                return Response([])
            req["nft"] = req["nft"][0].id
        favoriteItems = UserFavoritedNFT.objects.all().filter(**req)
        print(favoriteItems)
        # give the client exactly what they want
        # TODO: WRITE SOMETHING SMARTER here

        if "user" in req.keys() and "nft" not in req.keys():
            queryset = favoriteItems.values_list("nft", flat=True)
            nfts = NFT.objects.filter(pk__in=queryset)
            nftsData = NFTSerializer(nfts, many=True).data
            return Response(nftsData)
        elif "user" not in req.keys() and "nft" in req.keys():
            queryset = favoriteItems.values_list("user", flat=True)
            users = User.objects.filter(uAddress__in=queryset)
            usersData = UserSerializer(users, many=True).data
            return Response(usersData)
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
        reqData = request.GET.dict()
        watchListItems = UserWatchListedNFTCollection.objects.all().filter(**reqData)
        if "user" in reqData.keys() and "nftCollection" not in reqData.keys():
            queryset = watchListItems.values_list("nftCollection", flat=True)
            nftCollections = NFTCollection.objects.filter(name__in=queryset)

            nftCollections = NFTCollectionSerializer(nftCollections, many=True)
            return Response(nftCollections.data)
        elif "user" not in reqData.keys() and "nftCollection" in reqData.keys():
            queryset = watchListItems.values_list("user", flat=True)
            users = User.objects.filter(uAddress__in=queryset)
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
        queryset = UserWatchListedNFTCollection.objects.all().filter(**request.data)
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)


@api_view(["GET", "POST", "DELETE"])
def TransHistListView(request):
    if request.method == "GET":
        reqData = request.GET.dict()
        # print(reqData)
        if "UID" in reqData.keys() and "index" in reqData.keys():
            # print("INSIDE_____________")
            newReq = {}
            newReq["nft"] = NFT.objects.filter(UID=reqData["UID"], index=reqData["index"])
            if len(newReq["nft"]) == 0:
                return Response([])
            newReq["nft"] = newReq["nft"][0].id
            queryset = TransHist.objects.all().filter(**newReq)
            queryset = TransHistSerializer(queryset, many=True)
            return Response(queryset.data)
        else:
            # print("OUTSIDE_____________")
            queryset = TransHist.objects.all().filter(**request.GET.dict())
            queryset = TransHistSerializer(queryset, many=True)
            return Response(queryset.data)
    elif request.method == "POST":
        newTransHistObject = TransHistSerializer(data=request.data)
        newTransHistObject.is_valid(raise_exception=True)
        newTransHistObject.save()
        return Response(newTransHistObject.data)
    elif request.method == "DELETE":
        queryset = TransHist.objects.all().filter(**request.data)
        if len(queryset) == 0:
            return Response(status=400)
        queryset.delete()
        return Response(status=200)


@api_view(["GET"])
def HottestListView(request):
    if request.method == "GET":
        reqData = (
            request.GET.dict()
        )  # Will be given one of [nft, user, collection] and one of [DAY, MONTH, YEAR, ALLTIME]
        for i in reqData.keys():
            print(i)
        if "nft" in reqData.keys():
            transQuery = TransHist.objects.all()
            currentTime = date.today()
            if "DAY" in reqData.keys():
                transQuery = transQuery.filter(
                    time__year=currentTime.year, time__month=currentTime.month, time__day=currentTime.day
                )
            elif "MONTH" in reqData.keys():
                transQuery = transQuery.filter(time__year=currentTime.year, time__month=currentTime.month)
            elif "YEAR" in reqData.keys():
                transQuery = transQuery.filter(time__year=currentTime.year)
            valueSet = transQuery.values("nft").order_by().annotate(nft__count=Count("nft"))
            print(valueSet)
            finalSet = (valueSet.order_by("-nft__count")[:5]).values("nft")
            print(finalSet)
            queryset = NFT.objects.filter(id__in=finalSet)
            queryset = NFTSerializer(queryset, many=True)
            return Response(queryset.data)
        if "user" in reqData.keys():
            transQuery = TransHist.objects.all()
            currentTime = date.today()
            if "DAY" in reqData.keys():
                transQuery = transQuery.filter(
                    time__year=currentTime.year, time__month=currentTime.month, time__day=currentTime.day
                )
            elif "MONTH" in reqData.keys():
                transQuery = transQuery.filter(time__year=currentTime.year, time__month=currentTime.month)
            elif "YEAR" in reqData.keys():
                transQuery = transQuery.filter(time__year=currentTime.year)
            valueSet = transQuery.values("oldOwner").order_by().annotate(oldOwner__count=Count("oldOwner"))
            finalSet = valueSet.order_by("oldOwner__count")[:5]
            queryset = User.objects.filter(id__in=finalSet)
            queryset = NFTSerializer(queryset, many=True)
            return Response(queryset.data)
        if "collection" in reqData.keys():
            valueSet = NFTCollection.objects.all().order_by('-numLikes')[:5]
            print(valueSet)
            queryset = NFTCollectionSerializer(valueSet, many=True)
            return Response(queryset.data)
