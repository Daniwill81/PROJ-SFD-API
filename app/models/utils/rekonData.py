"""
Rekon data.

It can be a gorvment org or a private org.

"""
import pymongo

from sap.beanie import Document, Link

from app.models.sfd.sfd import Sfd
from app.models.criterias.criteria import Criteria
from app.models.utils.indicators import Indicator


class RekonData(Document):
    """
    Represents a ressources for indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    indicator: Link[Indicator] | None = None
    criteria: Link[Criteria]
    account_number: str
    amount: int
    year: int = 2024

    class Settings:
        """Settings for the database collection."""

        name = "rekondata"
        indexes = [
            # Ensure that there is no duplicate for account number
            pymongo.IndexModel([("account_number", pymongo.ASCENDING)], unique=True),
        ]
