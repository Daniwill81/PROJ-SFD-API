from app.models import RekonData, Sfd


async def rekon_data_create(
    sfd: Sfd,
    # name: str,
    account_number: str,
    amount: int,
    year: int = 2024,
) -> RekonData:
    """Create rekondata."""

    rekonData = await RekonData(sfd=sfd, account_number=account_number, amount=amount, year=year).create()
    return rekonData
