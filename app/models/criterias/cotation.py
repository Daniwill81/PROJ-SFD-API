"""
Cotations.

It can be a int or another type of data.

"""
from sap.beanie import Document, Link

from app.models.criterias.criteria import Criteria
from app.models.sfd.sfd import Sfd


class Cotation(Document):
    """
    Represents an cotation.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    criteria: Link[Criteria]
    mark: int
    year: int

    class Settings:
        """Settings for the database collection."""

        name = "cotation"
