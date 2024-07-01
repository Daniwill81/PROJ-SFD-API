"""
# Models.

Models define logical structuring of the data in the database.
"""
from .roledesc import RoleDesc
from .user import User

__all__ = [
    "RoleDesc",
    "User",
]
