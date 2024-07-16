"""
G;obal year result for a sfd.

It can be a gorvment org or a private org.

"""
import typing

from sap.beanie import Document, Link

from app.models.sfd.sfd import Sfd
from app.models.user.user import User


class GlobalYearResult(Document):
    """
    Represents an indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    user: Link[User]
    year: int
    data: dict[str, typing.Any]

    class Settings:
        """Settings for the database collection."""

        name = "globalyearresult"
