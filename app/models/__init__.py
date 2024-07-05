"""
# Models.

Models define logical structuring of the data in the database.
"""
from app.models.user.roledesc import RoleDesc
from app.models.user.user import User

__all__ = [
    "RoleDesc",
    "User",
]
