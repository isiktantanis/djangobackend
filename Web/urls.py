from django.urls import path

from . import views

app_name = "Web"

urlpatterns = [
    path("api/nfts", views.NFTListView.as_view(), name="NFT_home"),
    path("api/nftcollections", views.NFTCollectionListView.as_view(), name="NFTCollection_home"),
    path("api/users", views.UserListView.as_view(), name="User_home"),
    path("api/categories", views.CategoryListView.as_view(), name="Category_home"),
]
