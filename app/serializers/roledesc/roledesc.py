"""
# Serializers.

Handle data validation.
"""
import datetime

from sap.fastapi import ObjectSerializer

from app.models.utils.roledesc import RoleDesc


class RoleDescSerializer(ObjectSerializer[RoleDesc]):
    """Serialize the `organization` object for retrieve and listing."""

    id: str
    name: str
    acronym: str
    created: datetime.datetime

