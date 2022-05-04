from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import NFT, NFTCollection, NFTCollectionCategory, User

class UserAdminConfig(UserAdmin):
    model = User
    ordering = ('username',)
    list_display = ('uAddress','username', 'email', 'is_active', 'is_superuser', 'is_staff', 'date_joined')
    list_filter = ()
    fieldsets = ()
    exclude = ('last_login', 'date_joined')
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            'fields': ('uAddress', 'username', 'email', 'password1', 'password2', 'profilePicture', 'favoritedNFTs',
                       'watchListedNFTCollections', 'is_active', 'is_superuser', 'is_staff'),
        }),
    )




admin.site.register(User, UserAdminConfig)
admin.site.register(NFT, MPTTModelAdmin)
admin.site.register(NFTCollection, MPTTModelAdmin)
admin.site.register(NFTCollectionCategory, MPTTModelAdmin)

# Register your models here.
