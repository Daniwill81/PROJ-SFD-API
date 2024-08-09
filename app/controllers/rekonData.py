from app.models import Sfd, RekonData


async def rekonData_create(
    sfd: Sfd,
    account_number: str,
    amount: int,
    year: int = 2024,
) -> RekonData:
    """Create indicator."""

    rekonData = await RekonData(sfd=sfd, account_number=account_number, amount=amount, year=year).create()
    
    return rekonData