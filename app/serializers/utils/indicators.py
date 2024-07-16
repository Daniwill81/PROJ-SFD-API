"""
Serializers.

Handle data validation.
"""
import datetime
import typing

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
    ratio: int = 0
    mark: int = 0
    year: int = 2024
    created: datetime.datetime


class WriteIndicatorSerializer(WriteObjectSerializer[Indicator]):
    """Serialize the `indicator` object for create and update."""

    sfd: Sfd
    criteria: Criteria
    name: str
    ratio: int = 0
    mark: int = 0
    year: int = 2024

    # The fields bellow are not serialized
    instance: Indicator | None = None

    async def create(self, **kwargs: typing.Any) -> Indicator:
        """Create the object in the database using the data extracted by the serializer."""
        sfd: Sfd = kwargs["sfd"]
        criteria: Criteria = kwargs["criteria"]

        attributes = self.model_dump()
        attributes["name"] = str
        attributes["ratio"] = 0
        attributes["mark"] = 0
        attributes["year"] = 2024

        self.instance = await Indicator(**attributes, sfd=sfd, criteria=criteria).create()

        self.instance = await Indicator(**self.model_dump()).create()
        return self.instance
