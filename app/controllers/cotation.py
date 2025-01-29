from app.models import Cotation, Criteria, Sfd


async def cotation_create(sfd: Sfd, criteria: Criteria, mark: int, year: int = 2024) -> Cotation:
    """Create indicator."""

    cotation = await Cotation(sfd=sfd, criteria=criteria, mark=mark, year=year).create()

    return cotation
