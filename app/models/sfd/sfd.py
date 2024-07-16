"""
Sfd.

It can be a gorvment org or a private org.

"""
import pymongo

from sap.beanie import Document


class Sfd(Document):
    """
    Represents a sfd.

    It can be a int or another type of data.
    """

    name: str
    legal_form: str
    address: str
    category: str

    class Settings:
        """Settings for the database collection."""

        name = "sfd"
        indexes = [
            # Ensure that there is no duplicate for names
            pymongo.IndexModel([("name", pymongo.ASCENDING)], unique=True),
        ]
