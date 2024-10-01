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
    criteria: Link[Criteria] | None = None
    account_number: str
    amount: int
    year: int = 2024
