"""
Serializers.

Handle data validation.
"""
import datetime

from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.sfd.sfd import Sfd
from app.models.utils.rekonData import RekonData


class RekonDataSerializer(ObjectSerializer[RekonData]):
    """Serialize the rekondata object for retrieve and listing."""

    id: str
    sfd_id: str
    account_number: str
    amount: int
    year: int
    created: datetime.datetime


class WriteRekonDataSerializer(WriteObjectSerializer[RekonData]):
    """Serialize the `rekondata` object for create and update."""

    sfd: Sfd
    account_number: str
    amount: int
    year: int

    # The fields bellow are not serialized
    instance: RekonData | None = None
