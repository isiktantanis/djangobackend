from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import NFT, NFTCollection, User

admin.site.register(User, MPTTModelAdmin)
admin.site.register(NFT, MPTTModelAdmin)
admin.site.register(NFTCollection, MPTTModelAdmin)

# Register your models here.
