"""
Rekon data.

It can be a gorvment org or a private org.

"""
from sap.beanie import Document, Link

from app.models import Sfd, Criteria


class ThirdCrekonData(Document):
    """
    Represents a ressources for indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    criteria: Link[Criteria]
    n_year: int
    n_1_year: int
    name: str
    year: int = 2024

    class Settings:
        """Settings for the database collection."""

        name = "thirdcrekondata"
