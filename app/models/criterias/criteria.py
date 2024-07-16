"""
Criterias.

It can be a int or another type of data.

"""
import pymongo

from sap.beanie import Document


class Criteria(Document):
    """
    Represents an criteria.

    It can be a int or another type of data.
    """

    name: str
    mark: int

    class Settings:
        """Settings for the database collection."""

        name = "criteria"
        indexes = [
            # Ensure that there is no duplicate for names
            pymongo.IndexModel([("name", pymongo.ASCENDING)], unique=True),
            #
            pymongo.IndexModel(
                [
                    ("name", pymongo.TEXT),
                ],
                name="search",
            ),
        ]
