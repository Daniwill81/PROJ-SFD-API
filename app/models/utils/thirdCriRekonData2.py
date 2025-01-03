"""
Rekon data.

It can be a gorvment org or a private org.

"""
from sap.beanie import Document, Link

from app.models import Sfd, Criteria


class ThirdCrekonData2(Document):
    """
    Represents a ressources for indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name:str
    total_loan_amount: int
    net_asset: int
    year: int = 2024

    class Settings:
        """Settings for the database collection."""

        name = "thirdcrekondata2"
