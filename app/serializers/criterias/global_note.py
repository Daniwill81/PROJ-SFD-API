"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer

from app.models import GlobalNote, Sfd


class GlobalNoteSerializer(ObjectSerializer[GlobalNote]):
    """Serialize the cotation object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    risk_level: str
    mark: int
    year: int
    created: datetime.datetime
