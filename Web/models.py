from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.request import urlretrieve, urlcleanup
from django.core.files import File  # you need this somewhere
from django.utils.deconstruct import deconstructible
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
    uid = models.TextField(verbose_name=_("Unique ID"), primary_key=True)
    nID = models.IntegerField(verbose_name=_("ID"))
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    metaDataType = models.CharField(verbose_name=_("Metadata Type"), max_length=5,
                                    choices=[("video", "video"), ("audio", "audio"), ("image", "image")])
    dataLink = models.URLField(verbose_name=_("Data Link"))
    # take this link and move it to database and create another link
    # TODO: [NFTMAR-130] MAKE USERS DELETABLE WITHOUT EFFECTING NFTS
    collectionName = models.ForeignKey("NFTCollection", verbose_name=_("Collection Name"), on_delete=models.SET_NULL,
                                       null=True)
    creator = models.ForeignKey("User", related_name="creator", verbose_name=_("Creator"),
                                    on_delete=models.SET("USER_DELETED"))
    currentOwner = models.ForeignKey("User", verbose_name=_("Current Owner"),
                                     on_delete=models.SET("USER_DELETED"))
    marketStatus = models.IntegerField(verbose_name=_("Market Status"), default=0,
                                       choices=[(0, "Not On Market"), (1, "Not On Sale"), (2, "On Sale")])
    nftFile = models.FileField(upload_to="nfts/", blank=True, null=True, storage=OverwriteStorage(),
                               verbose_name=_("File"))
    numLikes = models.IntegerField(default=0, verbose_name=_("Number of Likes"))
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            name, ext = urlretrieve(self.dataLink)
            extension = ext['Content-Type'].split("/")[-1]  # not so sure that it'd always work
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

    # ADD LIKED BY NUMBER
class NFTCollection(MPTTModel):
    name = models.CharField(max_length=128, primary_key=True, verbose_name=_("Name"))
    collectionImage = models.ImageField(_("Collection Image"), null=True, blank=True, storage=OverwriteStorage(),
                                        upload_to=FileUploadLocation(parentFolder="NFTCollections/", fields=["name"]))
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    owner = models.ForeignKey("User", to_field="username", related_name="owner", verbose_name=_("Name"),
                              on_delete=models.SET("USER_DELETED"))
    category = models.ForeignKey("NFTCollectionCategory", to_field="name", related_name="category", null=True,
                                 verbose_name=_("Category of the NFT Collection."), on_delete=models.SET("USER_DELETED"))
    numLikes = models.IntegerField(default=0, verbose_name=_("Number of Likes"))

@receiver(models.signals.post_delete, sender=NFTCollection)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `NFTCollection` object is deleted.
    """
    if instance.collectionImage:
        if os.path.isfile(instance.collectionImage.path):
            os.remove(instance.collectionImage.path)

class NFTCollectionCategory(MPTTModel):
    name = models.CharField(_("Name"), primary_key=True, max_length=16)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class Meta:
        verbose_name_plural = "NFT Collection Categories"

class AccountManager(BaseUserManager):

    def create_superuser(self,  username, email, password, **other_fields):
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        return self.create_user(username, email, password, **other_fields)

    def create_user(self, username, email, password, **other_fields):
        # TODO: add more validations later?
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uAddress = models.TextField(_("Address"), primary_key=True)  # Address of the user coming from blockchain.
    username = models.CharField(_("Username"), max_length=32, unique=True)
    profilePicture = models.ImageField(_("Profile Picture"), null=True, blank=True, storage=OverwriteStorage(),
                                       upload_to=FileUploadLocation(parentFolder="profilePictures/", fields=["username"]))
    email = models.EmailField(_("Email"), unique=True, max_length=128)
    favoritedNFTs = models.ManyToManyField(NFT, blank=True)
    watchListedNFTCollections = models.ManyToManyField(NFTCollection, blank=True)
    # needed IF foreign key constraint is chosen to be settled like this
    is_active = models.BooleanField(_("Active"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)
    date_joined = models.DateTimeField(_("Join Date"), default=timezone.now, editable=False)
    objects = AccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.profilePicture:
        if os.path.isfile(instance.profilePicture.path):
            os.remove(instance.profilePicture.path)
