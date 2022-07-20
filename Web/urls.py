from django.urls import path

from . import views

app_name = "Web"

urlpatterns = [
    path("api/nfts/", views.NFTListView, name="NFT_home"),
    path(
        "api/nftcollections/",
        views.NFTCollectionListView,
        name="NFTCollection_home",
    ),
    path("api/users/", views.UserListView, name="User_home"),
    path("api/categories/", views.CategoryListView, name="Category_home"),
    path("api/favorites/", views.UserFavoritedNFTListView, name="Favorites_home"),
    path(
        "api/watchLists/",
        views.UserWatchListedNFTCollectionListView,
        name="WatchLists_home",
    ),
    path("api/transactionHistory/", views.TransHistListView, name="TransHistHome"),
    path("api/trending/user", views.TrendingUserListView, name="TrendingUsers"),
    path("api/trending/collection", views.TrendingCollectionListView, name="TrendingCollections"),
    path("api/trending/nft", views.TrendingNFTListView, name="TrendingNFTs"),

]
