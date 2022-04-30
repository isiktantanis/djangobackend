from django.urls import path

from . import views

app_name = "Web"

urlpatterns = [
    path("api/nfts", views.NFTListView, name="NFT_home"),
    path(
        "api/nftcollections",
        views.NFTCollectionListView,
        name="NFTCollection_home",
    ),
    path("api/users", views.UserListView, name="User_home"),
    path("api/categories", views.CategoryListView, name="Category_home"),
]
