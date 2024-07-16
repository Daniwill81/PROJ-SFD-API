"""
Serializers.

Handle data validation.
"""
import datetime

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
