"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.sfd.sfd import Sfd
from app.models.utils.rekonData import RekonData
from app.models.criterias.criteria import Criteria
from app.models.utils.indicators import Indicator


class RekonDataSerializer(ObjectSerializer[RekonData]):
    """Serialize the rekondata object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    indicator: Link[Indicator]
    account_number: str
    amount: int
    year: int = 2024
    created: datetime.datetime
