"""
Serializers.

Handle data validation.
"""
import datetime
import typing

from sap.beanie import Link
from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.controllers.utils import calculate_indicator_ratio_and_mark
from app.models import Criteria, Indicator, RekonData, Sfd


class IndicatorSerializer(ObjectSerializer[Indicator]):
    """Serialize the indicator object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    ratio: float = 0
    estimation: str = "Non necessaire pour cet indicateur"
    mark: int = 0
    year: int = 2024
    created: datetime.datetime
