"""
Users.

Users have access to the platform and can use it to perform actions.
Anyone that can log in to the platform is considered as a user.
"""

import typing

import passlib.pwd
import pydantic
import pymongo
import pymongo.collation
from beanie import operators

from sap.beanie import Document, Link
from sap.beanie.mixins import PasswordMixin

from app.models.enums import RoleEnum

from .roledesc import RoleDesc


class User(PasswordMixin, Document):
    """Represent a user of the platform."""

    roledesc: Link[RoleDesc]
    role: RoleEnum
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    password: str
    auth_key: str | None = None
    api_key: str | None = None

    def __str__(self) -> str:
        return f"l'utilisateur {self.first_name} {self.last_name.upper()}"

    def get_name(self) -> str:
        """Get full name of the user."""
        return f"{self.first_name} {self.last_name}"


    async def generate_auth_key(self) -> None:
        """Generate a random string for auth token."""
        await self.set({"auth_key": passlib.pwd.genword(length=32, charset="ascii_62")})

    async def generate_api_key(self) -> None:
        """Generate a random string for api token."""
        await self.set({"api_key": passlib.pwd.genword(length=32, charset="ascii_62")})

    @classmethod
    async def find_current(cls, email: str) -> typing.Self | None:
        """Retrieve user valid according to campaign."""
        return await User.find_one(
            operators.And(
                {User.email: email},
            )
        )


    class Settings:
        """Settings for the database collection."""

        name = "user"
        email_collation = pymongo.collation.Collation("en", strength=2)
        indexes = [
            pymongo.IndexModel([("email", pymongo.ASCENDING)], unique=True),
            pymongo.IndexModel("email", name="case_insensitive_email_index", collation=email_collation),
            pymongo.IndexModel(
                [
                    ("email", pymongo.TEXT),
                    ("first_name", pymongo.TEXT),
                    ("last_name", pymongo.TEXT),
                    ("password", pymongo.TEXT),
                ],
                name="search",
            ),
        ]
