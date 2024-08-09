"""
Serializers.

Handle data validation.
"""
import datetime

from sap.fastapi import ObjectSerializer
from sap.beanie import Link

from app.models import Cotation, Sfd, Criteria


class CotationSerializer(ObjectSerializer[Cotation]):
    """Serialize the cotation object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    mark: int
    year: int
    created: datetime.datetime
