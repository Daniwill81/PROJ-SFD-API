"""
# Models.

Models define logical structuring of the data in the database.
"""
from app.models.utils.roledesc import RoleDesc
from app.models.utils.user import User

__all__ = [
    "RoleDesc",
    "User",
]
