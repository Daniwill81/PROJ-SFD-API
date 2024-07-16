"""
Attachment for a sfd.

It can be a gorvment org or a private org.

"""

from sap.beanie import Document, Link

from app.models.sfd.sfd import Sfd


class Attachment(Document):
    """
    Represents an indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    type: str
    designation: str
    year: int

    class Settings:
        """Settings for the database collection."""

        name = "attachment"
