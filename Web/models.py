from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.request import urlretrieve, urlcleanup
from django.core.files import File  # you need this somewhere

# Function for renaming the upload name of image files

# Overrides the file with the same file name
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class NFT(MPTTModel):
    # ADD LIKED BY NUMBER
    uid = models.TextField(
        verbose_name=_("Unique ID"),
        primary_key=True,
    )
    nID = models.IntegerField(
        verbose_name=_("ID")
    )
    name = models.CharField(
        max_length=128,
        verbose_name=_("Name"),
    )
    description = models.TextField(verbose_name=_("Description"), null=True)
    metaDataType = models.CharField(verbose_name=_("metadata type"), choices=[("video", "video"), ("audio", "audio"), ("image", "image")], max_length=5)  # video, audio, image
    dataLink = models.URLField(verbose_name=_("data link"))
    # take this link and move it to database and create another link
    # TODO: [NFTMAR-130] MAKE USERS DELETABLE WITHOUT EFFECTING NFTS

    collectionName = models.ForeignKey(
        "NFTCollection",
        related_name="collectionName",
        verbose_name=_("Collection Name"),
        on_delete=models.SET_NULL,  # SOR
        null=True,
    )
    creatorName = models.ForeignKey(
        "User",
        to_field="username",
        related_name="creatorName",
        verbose_name=_("Creator"),
        on_delete=models.SET("user_deleted"),  # SOR
    )
    currentOwner = models.ForeignKey(
        "User",
        to_field="username",
        verbose_name=_("Current Owner"),
        on_delete=models.SET("user_deleted"),  # SOR
    )
    # 0: not on market, 1: on market but not on sale, 2: on market and on sale
    marketStatus = models.IntegerField(
        choices=[(0, "Not On Market"), (1, "Not On Sale"), (2, "On Sale")],
        verbose_name=_("Market Status"),
        default=0,
    )

    nftFile = models.FileField(
        upload_to="nfts/",
        blank=True,
        null=True,
        storage=OverwriteStorage(),
        verbose_name=_("File")
    )

    # slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    def save(self, *args, **kwargs):
        try:
            name, ext = urlretrieve(self.dataLink)
            extension = ext['Content-Type'].split("/")[-1]
            self.nftFile.save("{}/{}.{}".format(self.uid, self.nID, extension), File(open(name, 'rb')), False)
        finally:
            urlcleanup()
        super(NFT, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["uid", "nID"]


class NFTCollection(MPTTModel):
    name = models.CharField(max_length=128, primary_key=True, verbose_name=_("Name of the NFT collection."))
    # collectionImageLink = models.SlugField(verbose_name=_("Link of the image of collection"))
    # ADD LIKED BY NUMBER
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.TextField(
        verbose_name=_("Description of the NFT given by the creator."),
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        "User",
        to_field="username",
        related_name="owner",
        verbose_name=_("Name of the creator of the NFT Collection."),
        on_delete=models.SET("user_deleted"),  # SOR
        default="",
    )

    category = models.ForeignKey(
        "NFTCollectionCategory",
        to_field="name",
        related_name="category",
        verbose_name=_("Category of the NFT Collection."),
        on_delete=models.SET("user_deleted"),  # SOR
        null=True,
    )


class User(MPTTModel):

    uAdress = models.TextField(_("Address"), primary_key=True)  # Address of the user coming from blockchain.
    username = models.CharField(_("Username"), max_length=32, unique=True)
    profilePicture = models.ImageField(_("Profile Picture"), null=True, blank=True,
                                       upload_to="profilePictures/",
                                       storage=OverwriteStorage())
    mailAdress = models.TextField(_("Email"), unique=True)
    favoritedNFTs = models.ManyToManyField(NFT, blank=True)
    watchListedNFTCollections = models.ManyToManyField(NFTCollection, blank=True)

    password = models.CharField(
        _("Password"), max_length=100, null=False, default="0"
    )  # ADD SECURITY LATER lol
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")


class NFTCollectionCategory(MPTTModel):
    name = models.CharField(_("Name"), primary_key=True, max_length=16)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class Meta:
        verbose_name_plural = "NFT Collection Categories"
