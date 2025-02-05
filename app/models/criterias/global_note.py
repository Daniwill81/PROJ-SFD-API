"""
Cotations.

It can be a int or another type of data.

"""
from sap.beanie import Document, Link

from app.models.sfd.sfd import Sfd


class GlobalNote(Document):
    """
    Represents an cotation.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    risk_level: str
    mark: int
    year: int

    class Settings:
        """Settings for the database collection."""

        name = "globalNote"
