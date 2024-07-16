"""
Serializers.

Handle data validation.
"""
import datetime

from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.criterias.cotation import Cotation
from app.models.sfd.sfd import Sfd


class CotationSerializer(ObjectSerializer[Cotation]):
    """Serialize the cotation object for retrieve and listing."""

    id: str
    sfd_id: str
    sfd_name: str | None = None
    mark: int
    year: int
    created: datetime.datetime


class WriteCotationSerializer(WriteObjectSerializer[Cotation]):
    """Serialize the `user` object for create and update."""

    sfd: Sfd | None = None
    mark: int
    year: int

    # The fields bellow are not serialized
    instance: Cotation | None = None
