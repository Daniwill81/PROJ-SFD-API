"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer

from app.models import Cotation, Criteria, Sfd


class CotationSerializer(ObjectSerializer[Cotation]):
    """Serialize the cotation object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    mark: int
    year: int
    created: datetime.datetime
