"""
Serializers.

Handle data validation.
"""
import datetime

from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.sfd.sfd import Sfd


class SfdSerializer(ObjectSerializer[Sfd]):
    """Serialize the sfd object for retrieve and listing."""

    id: str
    name: str
    legal_form: str
    address: str
    year: int
    category: str
    created: datetime.datetime


class WriteSfdSerializer(WriteObjectSerializer[Sfd]):
    """Serialize the `sfd` object for create and update."""

    name: str
    legal_form: str
    address: str
    year: int
    category: str

    # The fields bellow are not serialized
    instance: Sfd | None = None
