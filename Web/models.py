from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class NFT(MPTTModel):
    # ADD LIKED BY NUMBER
    uid = models.TextField(
        # max_length= ???
        verbose_name=_("Unique id of the NFT."),
        primary_key=True,
    )
    nID = models.IntegerField(
        # max_length= ???
        verbose_name=_("ID of a certain NFT.")
    )
    name = models.CharField(
        max_length=128,
        verbose_name=_("NFT's name given by the NFT's creator."),
    )

    description = models.TextField(
        verbose_name=_("Description of the NFT given by the creator."), null=True
    )
    metaDataType = models.CharField(max_length=5, verbose_name=_("Type of the NFT."))
    dataLink = models.SlugField(verbose_name=_("Link of the content of NFT."))
    # take this link and move it to database and create another link
    # TODO: [NFTMAR-130] MAKE USERS DELETABLE WITHOUT EFFECTING NFTS

    collectionName = models.ForeignKey(
        "NFTCollection",
        related_name="collectionName",
        verbose_name=_("Name of the collection where the NFT belongs."),
        on_delete=models.SET_NULL,  # SOR
        null=True,
    )
    creatorName = models.ForeignKey(
        "User",
        to_field="username",
        related_name="creatorName",
        verbose_name=_("Name of the creator of the NFT."),
        on_delete=models.SET("user_deleted"),  # SOR
    )
    currentOwner = models.ForeignKey(
        "User",
        to_field="username",
        verbose_name=_("Name of the owner of the NFT."),
        on_delete=models.SET("user_deleted"),  # SOR
    )
    marketStatus = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        verbose_name=_(
            "0: not on market, 1: on market but not on sale, 2: on market and on sale"
        ),
        default=0,
    )

    # slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    # attributes

    class Meta:
        unique_together = ["uid", "nID"]


class NFTCollection(MPTTModel):
    name = models.CharField(
        max_length=128, primary_key=True, verbose_name=_("Name of the NFT collection.")
    )
    # collectionImageLink = models.SlugField(verbose_name=_("Link of the image of collection"))
    # ADD LIKED BY NUMBER
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
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
    uAdress = models.TextField(
        _("Address of the user coming from blockchain."), primary_key=True
    )
    username = models.CharField(
        _("Unique name of the user set when signing up"), max_length=32, unique=True
    )
    profilePicture = models.ImageField(
        _("User's profile picture"), null=True, blank=True, upload_to="media/"
    )
    mailAdress = models.TextField(
        _("Mail address of the user set when signing up"), unique=True
    )
    favoritedNFTs = models.ManyToManyField(NFT, blank=True)
    watchListedNFTCollections = models.ManyToManyField(NFTCollection, blank=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    password = models.CharField(
        _("Password of user"), max_length=100, null=False, default="0"
    )  # ADD SECURITY LATER lol


class NFTCollectionCategory(MPTTModel):
    name = models.CharField(
        _("Name of the NFT Collection Category."), primary_key=True, max_length=16
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class Meta:
        verbose_name_plural = "NFT Collection Categories"
