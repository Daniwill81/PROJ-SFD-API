"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer

from app.models import Criteria, ThirdCrekonData2, Sfd


class ThirdCRekonData2Serializer(ObjectSerializer[ThirdCrekonData2]):
    """Serialize the indicator object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    total_loan_amount: int
    net_asset: int
    ratio: float = 0
    mark: int = 0
    year: int = 2024
    created: datetime.datetime
