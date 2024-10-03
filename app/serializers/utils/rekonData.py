"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer

from app.models.sfd.sfd import Sfd
from app.models.utils.rekonData import RekonData


class RekonDataSerializer(ObjectSerializer[RekonData]):
    """Serialize the rekondata object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    account_number: str
    amount: int
    year: int = 2024
    created: datetime.datetime
