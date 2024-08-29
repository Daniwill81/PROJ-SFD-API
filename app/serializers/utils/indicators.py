"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer

from app.models import Criteria, Indicator, Sfd


class IndicatorSerializer(ObjectSerializer[Indicator]):
    """Serialize the indicator object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    ratio: int = 0
    mark: int = 0
    year: int = 2024
    created: datetime.datetime
