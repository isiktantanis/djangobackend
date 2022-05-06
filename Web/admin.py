from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mptt.admin import MPTTModelAdmin

from .models import (
    NFT,
    NFTCollection,
    NFTCollectionCategory,
    TransHist,
    User,
    UserFavoritedNFT,
    UserWatchListedNFTCollection,
)


class UserAdminConfig(UserAdmin):
    model = User
    ordering = ("username",)
    list_display = ("uAddress", "username", "email", "is_active", "is_superuser", "is_staff", "date_joined")
    list_filter = ()
    fieldsets = ()
    exclude = ("last_login", "date_joined")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "uAddress",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "profilePicture",
                    "is_active",
                    "is_superuser",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(NFT, MPTTModelAdmin)
admin.site.register(NFTCollection, MPTTModelAdmin)
admin.site.register(NFTCollectionCategory, MPTTModelAdmin)
admin.site.register(UserFavoritedNFT, MPTTModelAdmin)
admin.site.register(UserWatchListedNFTCollection, MPTTModelAdmin)
admin.site.register(TransHist, MPTTModelAdmin)

# Register your models here.
