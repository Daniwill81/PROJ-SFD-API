"""
Enums.

Platforme users role enumeration.
"""
import enum


class RoleEnum(str, enum.Enum):
    """List of roles available for users.

    Each role has different access and set of permissions.
    """

    ADMIN = "ADMIN"  # SFD - Super-administrateur
    INSPECTEUR = "INSPECTEUR"  # SFD - inspecteur

    @classmethod
    def get_list_primary(cls) -> list["RoleEnum"]:
        """Get the list of primary users."""
        return [
            cls.ADMIN,
            cls.INSPECTEUR,
        ]


class SexEnum(str, enum.Enum):
    """Sex of users"""

    M = "Male"
    F = "Female"
