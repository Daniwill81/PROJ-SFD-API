"""
Organizations.

It can be a government institution, or a travel company, or a bank, etc...
All users in the system are tied to an organization.
Organization is useful in defining the role of each user.
"""
import pymongo

from sap.beanie import Document, Link

from app.models.enums import RoleTypeEnum, RoleEnum


class RoleDesc(Document):
    """
    Represents a role.

    It can be a inspector or an admin.
    """

    name: str
    acronym: str
    type: RoleTypeEnum


    def get_acronym(self) -> str:
        """Return the acronym."""
        return self.acronym

    def get_role(self) -> RoleEnum:
        """Get the role according to the organization and wether is primary user or not."""
        code: str

        if self.acronym:
            code = self.acronym
            code += "1"

        return RoleEnum[code]


    class Settings:
        """Settings for the database collection."""

        name = "roledesc"
        indexes = [
            # Ensure that there is no duplicate for names
            pymongo.IndexModel([("name", pymongo.ASCENDING)], unique=True),
            #
            # Ensure that there is no duplicate for Govs institutions
            # only check uniqueness when non null
            pymongo.IndexModel("acronym", unique=True, partialFilterExpression={"acronym": {"$type": "string"}}),
            pymongo.IndexModel(
                [
                    ("name", pymongo.TEXT),
                    ("acronym", pymongo.TEXT),
                ],
                name="search",
            ),
        ]
