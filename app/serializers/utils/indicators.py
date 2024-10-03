"""
Serializers.

Handle data validation.
"""
import datetime
import typing

from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from sap.beanie import Link
from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.controllers.utils import calculate_indicator_ratio_and_mark
from app.models import Criteria, Indicator, RekonData, Sfd


class IndicatorSerializer(ObjectSerializer[Indicator]):
    """Serialize the indicator object for retrieve and listing."""

    id: str
    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    ratio: float = 0
    mark: int = 0
    year: int = 2024
    created: datetime.datetime


class WriteIndicatorSerializer(WriteObjectSerializer[Indicator]):
    """Serialize the `indicator` object for create and update."""

    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    ratio: float = 0
    mark: int = 0
    year: int = 2024

    # The fields below are not serialized
    instance: Indicator | None = None

    @staticmethod
    async def calculate_ratio_and_mark(indicator: Indicator) -> typing.Union[float, int]:
        """Calculate the ratio for the given indicator."""
        # Fetch all RekonData for this indicator's SFD and year
        rekon_data_list = await RekonData.find(
            RekonData.sfd == indicator.sfd, RekonData.year == indicator.year
        ).to_list()

        # Calculate the ratio using the utility function
        return calculate_indicator_ratio_and_mark(indicator, rekon_data_list)

    async def create(self, **kwargs: typing.Any) -> Indicator:
        """Create the object in the database using the data extracted by the serializer."""
        # Create the indicator instance
        self.instance = await Indicator(**self.model_dump()).create()

        # Calculate and update the ratio if possible
        calculated_ratio, calculated_mark = await self.calculate_ratio_and_mark(self.instance)
        if calculated_ratio is not None and calculated_mark is not None:
            self.instance.ratio = calculated_ratio
            self.instance.mark = calculated_mark
            await self.instance.save()

        return self.instance
