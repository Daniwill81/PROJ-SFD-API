"""
Enums.

Platforme users role enumeration.
"""
import enum


class RoleTypeEnum(str, enum.Enum):
    """The type of institution.

    Government institution have many types.
    This is because each institution plays a different role.
    """

    ADMIN = "ADMIN"  # SFD - Super-administrateur
    INSP = "INSP"  # SFD - Super-inspecteur


class RoleEnum(str, enum.Enum):
    """List of roles available for users.

    Each role has different access and set of permissions.
    """

    ADMIN1 = "ADMIN1"  # SFD - Super-administrateur
    INSP1 = "INSP1"  # SFD - inspecteur

    @classmethod
    def get_list_primary(cls) -> list["RoleEnum"]:
        """Get the list of primary users."""
        return [
            cls.ADMIN1,
            cls.INSP1,
        ]


class SexEnum(str, enum.Enum):
    """The sex of the person."""

    M = "M"  # Male
    F = "F"  # Female
