from app.models import Criteria, Indicator, Sfd


async def indicator_create(
    sfd: Sfd, criteria: Criteria, name: str, ratio: int = 0, mark: int = 0, year: int = 2024
) -> Indicator:
    """Create indicator."""

    indicator = await Indicator(sfd=sfd, criteria=criteria, name=name, ratio=ratio, mark=mark, year=year).create()

    return indicator
