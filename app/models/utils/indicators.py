"""
Indicators.

It can be a gorvment fin org or a private fin org.

"""

from sap.beanie import Document, Link

from app.models.criterias.criteria import Criteria
from app.models.sfd.sfd import Sfd


class Indicator(Document):
    """
    Represents an indicators.

    It can be a int or another type of data.
    """

    sfd: Link[Sfd]
    criteria: Link[Criteria]
    name: str
    ratio: float = 0
    estimation: str = "Non necessaire pour cet indicateur"
    mark: int = 0
    year: int = 2024

    @classmethod
    async def get_total_mark_by_sfd_criteria_and_year(cls, sfd: str, criteria: str, year: int) -> int:
        """
        Calcule la somme des marks des indicateurs pour un SFD, un critère et une année donnés.
        """
        pipeline = [
            {"$match": {"sfd": sfd, "criteria": criteria, "year": year}},
            {"$group": {"_id": None, "total_mark": {"$sum": "$mark"}}},
        ]
        result = await cls.aggregate(pipeline).to_list()
        return result[0]["total_mark"] if result else 0

    class Settings:
        """Settings for the database collection."""

        name = "indicator"
