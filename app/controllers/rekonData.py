from app.models import RekonData, Sfd
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status


async def rekonData_create(
    sfd: Sfd,
    account_number: str,
    amount: int,
    year: int = 2024,
) -> RekonData:
    """Create rekondata."""

    try:
        rekonData = await RekonData(sfd=sfd, account_number=account_number, amount=amount, year=year).create()
        return rekonData
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"RekonData with account_number '{account_number}' already exists."
        )
