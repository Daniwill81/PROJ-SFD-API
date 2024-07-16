"""
Serializers.

Handle data validation.
"""
import datetime

from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.criterias.criteria import Criteria
from app.models.sfd.sfd import Sfd
from app.models.utils.indicators import Indicator


class IndicatorSerializer(ObjectSerializer[Indicator]):
    """Serialize the indicator object for retrieve and listing."""

    id: str
    sfd_id: str
    criteria_id: str
    name: str
    ratio: int | None = None
    mark: int | None = None
    year: int
    created: datetime.datetime


class WriteIndicatorSerializer(WriteObjectSerializer[Indicator]):
    """Serialize the `indicator` object for create and update."""

    sfd: Sfd
    criteria: Criteria
    name: str
    ratio: int | None = None
    mark: int | None = None
    year: int

    # The fields bellow are not serialized
    instance: Indicator | None = None
