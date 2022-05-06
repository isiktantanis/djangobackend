import os
from urllib.request import urlcleanup, urlretrieve

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files import File  # you need this somewhere
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


# Class for renaming the upload name of image files
@deconstructible
class FileUploadLocation(object):
    def __init__(self, parentFolder, fields):
        self.parentFolder = parentFolder
        self.fields = fields

    def __call__(self, instance, filename):
        directoryWRTFields = ""
        for field in self.fields:
            if field in instance.__dict__.keys():
                directoryWRTFields += "{}/".format(instance.__dict__[field])
            else:
                directoryWRTFields += "{}/".format(field)
        directoryWRTFields = directoryWRTFields[:-1]
        return "{}/{}.{}".format(self.parentFolder, directoryWRTFields, filename.split(".")[-1])


# Overrides the file with the same file name
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class NFT(MPTTModel):
    UID = models.TextField(verbose_name=_("Unique ID"))
    index = models.IntegerField(verbose_name=_("index"))
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    metaDataType = models.CharField(
        verbose_name=_("Metadata Type"),
        max_length=5,
        choices=[("video", "video"), ("audio", "audio"), ("image", "image")],
    )
    dataLink = models.URLField(verbose_name=_("Data Link"))
    # take this link and move it to database and create another link
    # TODO: [NFTMAR-130] MAKE USERS DELETABLE WITHOUT EFFECTING NFTS
    collectionName = models.ForeignKey(
        "NFTCollection", verbose_name=_("Collection Name"), on_delete=models.SET_NULL, null=True
    )
    creator = models.ForeignKey(
        "User", related_name="creator", verbose_name=_("Creator"), on_delete=models.SET("USER_DELETED")
    )
    currentOwner = models.ForeignKey("User", verbose_name=_("Current Owner"), on_delete=models.SET("USER_DELETED"))
    marketStatus = models.IntegerField(
        verbose_name=_("Market Status"), default=0, choices=[(0, "Not On Market"), (1, "Not On Sale"), (2, "On Sale")]
    )
    nftFile = models.FileField(
        upload_to="nfts/", blank=True, null=True, storage=OverwriteStorage(), verbose_name=_("File")
    )
    numLikes = models.IntegerField(default=0, verbose_name=_("Number of Likes"))
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", editable=False
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            name, ext = urlretrieve(self.dataLink)
            extension = ext["Content-Type"].split("/")[-1]  # not so sure that it'd always work
            self.nftFile.save("{}/{}.{}".format(self.UID, self.index, extension), File(open(name, "rb")), False)
        finally:
            urlcleanup()
        super(NFT, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["UID", "index"]


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
            directoryPath = instance.nftFile.path[: instance.nftFile.path.rfind("/")]
            if len(os.listdir(directoryPath)) == 0:
                os.rmdir(directoryPath)

    # ADD LIKED BY NUMBER


class NFTCollection(MPTTModel):
    name = models.CharField(max_length=128, primary_key=True, verbose_name=_("Name"))
    collectionImage = models.ImageField(
        _("Collection Image"),
        null=True,
        blank=True,
        storage=OverwriteStorage(),
        upload_to=FileUploadLocation(parentFolder="NFTCollections/", fields=["name"]),
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", editable=False
    )
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    owner = models.ForeignKey(
        "User", to_field="username", related_name="NFTCollection", verbose_name=_("Owner"),
        on_delete=models.SET("USER_DELETED"))
    category = models.ForeignKey(
        "NFTCollectionCategory",
        to_field="name",
        related_name="category",
        null=True,
        verbose_name=_("Category of the NFT Collection."),
        on_delete=models.SET("USER_DELETED"),
    )
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
    backgroundPicture = models.ImageField(_("Background Picture"), storage=OverwriteStorage(),
                                          upload_to=FileUploadLocation(parentFolder="Categories/",
                                                                       fields=["name", "background"]))
    foregroundPicture = models.ImageField(_("Foreground Picture"), storage=OverwriteStorage(),
                                          upload_to=FileUploadLocation(parentFolder="Categories/",
                                                                       fields=["name", "foreground"]))
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", editable=False
    )

    class Meta:
        verbose_name_plural = "NFT Collection Categories"


@receiver(models.signals.post_delete, sender=NFTCollectionCategory)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `NFTCollectionCategory` object is deleted.
    """
    if instance.backgroundPicture:
        if os.path.isfile(instance.backgroundPicture.path):
            os.remove(instance.backgroundPicture.path)

    if instance.foregroundPicture:
        if os.path.isfile(instance.foregroundPicture.path):
            os.remove(instance.foregroundPicture.path)


class AccountManager(BaseUserManager):
    def create_superuser(self, username, email, password, **other_fields):
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


# TODO: [NFTMAR-149] Kill the Old Access Tokens After Refreshing Using the Refresh Token


class User(AbstractBaseUser, PermissionsMixin):
    uAddress = models.TextField(_("Address"), primary_key=True)  # Address of the user coming from blockchain.
    username = models.CharField(_("Username"), max_length=32, unique=True)
    profilePicture = models.ImageField(
        _("Profile Picture"),
        null=True,
        blank=True,
        storage=OverwriteStorage(),
        upload_to=FileUploadLocation(parentFolder="profilePictures/", fields=["username"]),
    )
    email = models.EmailField(_("Email"), unique=True, max_length=128)
    # needed IF foreign key constraint is chosen to be settled like this
    is_active = models.BooleanField(_("Active"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)
    date_joined = models.DateTimeField(_("Join Date"), default=timezone.now, editable=False)
    objects = AccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "uAddress"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.is_active:
            if self.profilePicture:
                if os.path.isfile(self.profilePicture.path):
                    os.remove(self.profilePicture.path)
        super(User, self).save(*args, **kwargs)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `User` object gets deactivated.
    """
    try:
        old_user = sender.objects.get(pk=instance.pk)
        if old_user.profilePicture and not instance.is_active and old_user.is_active:
            if os.path.isfile(old_user.profilePicture.path):
                os.remove(old_user.profilePicture.path)
    except:
        pass


class UserFavoritedNFT(MPTTModel):
    user = models.ForeignKey("User", related_name="likes", verbose_name=_("User"), on_delete=models.CASCADE)
    nft = models.ForeignKey("NFT", related_name="likedBy", verbose_name=_("NFT"), on_delete=models.CASCADE)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", editable=False
    )

    def __str__(self):
        return "{}-{}".format(self.user, self.nft)

    class Meta:
        unique_together = ["user", "nft"]
        db_table = "Favorites"

    # TODO: CHECK IF SENDING THE SAME REQUEST EFFECTS ANYTHING?
    def save(self, *args, **kwargs):
        self.nft.numLikes += 1
        self.nft.save()
        super(UserFavoritedNFT, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=UserFavoritedNFT)
def decrease_like(sender, instance, **kwargs):
    if instance.nft:
        instance.nft.numLikes -= 1
        instance.nft.save()


class UserWatchListedNFTCollection(MPTTModel):
    user = models.ForeignKey("User", related_name="watchListed", verbose_name=_("User"), on_delete=models.CASCADE)
    nftCollection = models.ForeignKey(
        "NFTCollection", related_name="watchListedBy", verbose_name=_("NFT Collection"), on_delete=models.CASCADE
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", editable=False
    )

    def __str__(self):
        return "{}-{}".format(self.user, self.nftCollection)

    class Meta:
        unique_together = ["user", "nftCollection"]
        db_table = "WatchLists"

    def save(self, *args, **kwargs):
        self.nftCollection.numLikes += 1
        self.nftCollection.save()
        super(UserWatchListedNFTCollection, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=UserWatchListedNFTCollection)
def decrease_like(sender, instance, **kwargs):
    if instance.nftCollection:
        instance.nftCollection.numLikes -= 1
        instance.nftCollection.save()


class TransHist(MPTTModel):
    oldOwner = models.ForeignKey("User", related_name="oldUser", verbose_name=_("Old User"), on_delete=models.CASCADE)
    newOwner = models.ForeignKey("User", related_name="newUser", verbose_name=_("New User"), on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name=_("Price"), validators=[MinValueValidator(1)])
    time = models.DateTimeField(_("Time of Transaction"), default=timezone.now)
    nft = models.ForeignKey("NFT", related_name="nft", verbose_name=_("NFT"), on_delete=models.CASCADE)

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", editable=False
    )
