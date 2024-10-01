"""
Rekon data.

It can be a gorvment org or a private org.

"""
import pymongo

from sap.beanie import Document, Link

from app.models.sfd.sfd import Sfd


class RekonData(Document):
    """
    Represents a ressources for indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    name: str | None = None
    account_number: str
    amount: int
    year: int = 2024

    class Settings:
        """Settings for the database collection."""

        name = "rekondata"
        indexes = [
            # Ensure that there is no duplicate for account_number
            pymongo.IndexModel([("name", pymongo.ASCENDING)], unique=True),
        ]
