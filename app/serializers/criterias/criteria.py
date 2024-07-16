"""
Serializers.

Handle data validation.
"""
import datetime
import typing

from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.criterias.criteria import Criteria


class CriteriaSerializer(ObjectSerializer[Criteria]):
    """Serialize the criteria object for retrieve and listing."""

    id: str
    mark: int
    name: str
    created: datetime.datetime


class WriteCriteriaSerializer(WriteObjectSerializer[Criteria]):
    """Serialize the `user` object for create and update."""

    name: str
    mark: int

    # The fields bellow are not serialized
    instance: Criteria | None = None

    async def create(self, **kwargs: typing.Any) -> Criteria:
        """Create the object in the database using the data extracted by the serializer."""

        self.instance = await Criteria(**self.model_dump()).create()
        return self.instance
