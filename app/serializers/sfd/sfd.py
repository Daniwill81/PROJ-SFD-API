"""
Serializers.

Handle data validation.
"""
import datetime
import typing

from sap.fastapi import ObjectSerializer, WriteObjectSerializer

from app.models.sfd.sfd import Sfd


class SfdSerializer(ObjectSerializer[Sfd]):
    """Serialize the sfd object for retrieve and listing."""

    id: str
    name: str
    legal_form: str
    address: str
    category: str
    created: datetime.datetime


class WriteSfdSerializer(WriteObjectSerializer[Sfd]):
    """Serialize the `sfd` object for create and update."""

    name: str
    legal_form: str
    address: str
    category: str

    # The fields bellow are not serialized
    instance: Sfd | None = None

    async def create(self, **kwargs: typing.Any) -> Sfd:
        """Create the object in the database using the data extracted by the serializer."""

        self.instance = await Sfd(**self.model_dump()).create()
        return self.instance
