from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.request import urlretrieve, urlcleanup
from django.core.files import File  # you need this somewhere
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver

# Class for renaming the upload name of image files
@deconstructible
class FileUploadLocation(object):
    def __init__(self, parentFolder, fields):
        self.parentFolder = parentFolder
        self.fields = fields

    def __call__(self, instance, filename):
        directoryWRTFields = ""
        for field in self.fields:
            directoryWRTFields += "{}/".format(instance.__dict__[field])
        directoryWRTFields = directoryWRTFields[:-1]
        return "{}/{}.{}".format(self.parentFolder, directoryWRTFields, filename.split(".")[-1])

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
    metaDataType = models.CharField(verbose_name=_("metadata type"),
                                    choices=[("video", "video"), ("audio", "audio"), ("image", "image")], max_length=5)
    dataLink = models.URLField(verbose_name=_("data link"))
    # take this link and move it to database and create another link
    # TODO: [NFTMAR-130] MAKE USERS DELETABLE WITHOUT EFFECTING NFTS

    collectionName = models.ForeignKey(
        "NFTCollection",
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

@receiver(models.signals.post_delete, sender=NFT)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.nftFile:
        if os.path.isfile(instance.nftFile.path):
            os.remove(instance.nftFile.path)
            # remove the directory of the file is the directory is empty
            directoryPath = instance.nftFile.path[:instance.nftFile.path.rfind("/")]
            if len(os.listdir(directoryPath)) == 0:
                os.rmdir(directoryPath)


class NFTCollection(MPTTModel):
    name = models.CharField(max_length=128, primary_key=True, verbose_name=_("Name"))
    # collectionImageLink = models.SlugField(verbose_name=_("Link of the image of collection"))
    # ADD LIKED BY NUMBER
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
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
    uAddress = models.TextField(_("Address"), primary_key=True)  # Address of the user coming from blockchain.
    username = models.CharField(_("Username"), max_length=32, unique=True)
    profilePicture = models.ImageField(_("Profile Picture"), null=True, blank=True, storage=OverwriteStorage(),
                                       upload_to=FileUploadLocation(parentFolder="profilePictures/", fields=["username"]))
    mailAddress = models.EmailField(_("Email"), unique=True, max_length=128)
    favoritedNFTs = models.ManyToManyField(NFT, blank=True)
    watchListedNFTCollections = models.ManyToManyField(NFTCollection, blank=True)

    password = models.CharField(
        _("Password"), max_length=100, null=False, default="0"
    )  # ADD SECURITY LATER lol
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.profilePicture:
        if os.path.isfile(instance.profilePicture.path):
            os.remove(instance.profilePicture.path)



class NFTCollectionCategory(MPTTModel):
    name = models.CharField(_("Name"), primary_key=True, max_length=16)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class Meta:
        verbose_name_plural = "NFT Collection Categories"
