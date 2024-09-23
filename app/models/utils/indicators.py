"""
Indicators.

It can be a gorvment fin org or a private fin org.

"""
import pymongo

from sap.beanie import Document, Link

from app.models.criterias.criteria import Criteria
from app.models.sfd.sfd import Sfd


class Indicator(Document):
    """
    Represents an indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    ratio: int | None = None
    mark: int | None = None
    year: int = 2024

    class Settings:
        """Settings for the database collection."""

        name = "indicator"
        indexes = [
            # Ensure that there is no duplicate for names
            pymongo.IndexModel([("name", pymongo.ASCENDING)], unique=True),
        ]
