"""
# Models.

Models define logical structuring of the data in the database.
"""
from app.models.criterias.cotation import Cotation
from app.models.criterias.criteria import Criteria
from app.models.sfd.attachment import Attachment
from app.models.sfd.global_year_result import GlobalYearResult
from app.models.sfd.sfd import Sfd
from app.models.user.user import User
from app.models.utils.indicators import Indicator
from app.models.utils.rekonData import RekonData
from app.models.utils.thirdCriRekonData import ThirdCrekonData


__all__ = [
    "User",
    "Criteria",
    "Cotation",
    "Attachment",
    "GlobalYearResult",
    "Sfd",
    "Indicator",
    "RekonData",
    "ThirdCrekonData",
]
