"""
Serializers.

Handle data validation.
"""
import datetime

from sap.beanie import Link
from sap.fastapi import ObjectSerializer

from app.models import Sfd, ThirdCrekonData


class ThirdCRekonDataSerializer(ObjectSerializer[ThirdCrekonData]):
    """Serialize the indicator object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    n_year: int
    n_1_year: int
    account_number: str
    total_loan_amount: int
    net_asset: int
    year: int = 2024
    created: datetime.datetime
