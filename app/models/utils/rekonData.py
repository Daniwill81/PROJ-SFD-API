"""
Rekon data.

It can be a gorvment org or a private org.

"""
from sap.beanie import Document, Link
from typing import Optional
from pydantic import Field

from app.models.sfd.sfd import Sfd


class RekonData(Document):
    """
    Represents a ressources for indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    account_number: str
    description: str
    amount: int
    year: int = 2024

    class Settings:
        """Settings for the database collection."""

        name = "rekondata"
