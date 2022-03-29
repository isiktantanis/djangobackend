from asyncio.windows_events import NULL
from enum import unique
from ftplib import FTP

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from pyexpat import model

# Create your models here.


class NFT(MPTTModel):
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

    description = models.TextField(verbose_name=_("Description of the NFT given by the creator."), null=True)
    metaDataType = models.CharField(max_length=5, verbose_name=_("Type of the NFT."))
    dataLink = models.TextField(verbose_name=_("Link of the content of NFT."))
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
        verbose_name=_("0: not on market, 1: on market but not on sale, 2: on market and on sale"),
    )

    # attributes

    class Meta:
        unique_together = ["uid", "nID"]


class NFTCollection(MPTTModel):
    name = models.CharField(max_length=128, primary_key=True, verbose_name=_("Name of the NFT collection."))


class User(MPTTModel):
    uAdress = models.TextField(_("Address of the user coming from blockchain."), primary_key=True)
    username = models.CharField(_("Unique name of the user set when signing up"), max_length=32, unique=True)
    profilePicture = models.ImageField(_("User's profile picture"), null=True, upload_to="media/")
    mailAdress = models.TextField(_("Mail address of the user set when signing up"), unique=True)
    favoritedNFTs = models.ManyToManyField(NFT)
    watchListedNFTCollections = models.ManyToManyField(NFTCollection)
