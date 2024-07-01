"""
# Serializers.

Handle data validation.
"""

import datetime
import typing

import pydantic
from pydantic import Field

from sap.fastapi import ObjectSerializer, WriteObjectSerializer
from sap.fastapi.auth import JWTAuth

from app.models.utils.user import User
from app.models.utils.roledesc import RoleDesc
from app.models.enums import RoleEnum
from app.xlib.utils import get_frontend_url


class UserSerializer(ObjectSerializer[User]):
    """Serialize the `user` object for retrieve and listing."""

    id: str
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    role: RoleEnum
    created: datetime.datetime


class WriteUserSerializer(WriteObjectSerializer[User]):
    """Serialize the `user` object for create and update."""

    first_name: str
    last_name: str
    email: pydantic.EmailStr
    roledesc: RoleDesc | None = None
    role: RoleEnum | None = None

    # The fields bellow are not serialized
    instance: User | None = None

    async def run_async_validators(self, **kwargs: typing.Any) -> None:
        """Check that data pass DB validation."""
        await self.validate_email_uniqueness()
        await self.validate_role()

    async def validate_email_uniqueness(self) -> None:
        """Check that the email is not used by another user."""
        if self.instance and self.instance.email == self.email:
            return

        is_duplicate = await User.find_current(email=self.email)
        if is_duplicate:
            raise AssertionError("Cet email est déjà rattaché à un compte administrateur existant.")

    async def validate_role(self) -> None:
        """Set user role."""
        self.role = self.instance.role if self.instance else None

##########################################################################################################
    async def create(self, **kwargs: typing.Any) -> User:
        """Create the object in the database using the data extracted by the serializer."""
        assert self.roledesc
        request_user: User = kwargs["request_user"]
        is_primary = bool(request_user.role)

        self.role = self.organization.get_role(is_primary=is_primary)
        assert self.role, "Role not provided"
        campaign = Campaign.get_default() if self.role in [RoleEnum.SA1, RoleEnum.SA2] else None
        self.instance = await User(**self.model_dump(), is_primary=is_primary, campaign=campaign).create()
        assert self.instance.role, "Role not set"
        return self.instance
###########################################################################################################

    async def update(self, **kwargs: typing.Any) -> User:
        """Update the object in the database using the data extracted by the serializer."""
        assert self.instance
        data_to_update = {"first_name": self.first_name, "last_name": self.last_name, "email": self.email}
        instance: User = self.instance.model_copy(update=data_to_update)
        await instance.save()
        self.instance = instance
        return instance


class APIKeySerializer(ObjectSerializer[User]):
    """Serializer the `APIKey` object that depends on the User object."""

    id: str
    api_key: str
