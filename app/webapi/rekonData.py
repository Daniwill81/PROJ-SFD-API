"""
# WebAPI.

The API endpoint  is queried by other applications
to communicate with this application. This endpoint usually relies
on a header based authenticated encoded in the request headers.
Commonly Basic or Bearer Auth.

It should accept and returns data formatted in JSON.

The API is structured with  Representational state transfer architecture:
https://en.wikipedia.org/wiki/Representational_state_transfer
"""

from fastapi import APIRouter, Depends, Request, status

from sap.fastapi.pagination import CursorInfo, PaginatedData

from app import controllers
from app.models.enums import RoleEnum
from app.models.user.auth import user_auth
from app.models.user.user import User
from app.models.utils.rekonData import RekonData
from app.serializers.utils.rekonData import RekonDataSerializer

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    rekonData: RekonData,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> RekonDataSerializer:
    """Create a indicator."""
    sfd = rekonData.sfd
    account_number = rekonData.account_number
    amount = rekonData.amount
    year = rekonData.year

    await controllers.rekonData.rekonData_create(sfd=sfd, account_number=account_number, amount=amount, year=year)
    instance = rekonData

    return RekonDataSerializer.read(instance)


@router.get("/{pk}/", status_code=status.HTTP_200_OK)
async def retrieve(
    pk: str,
) -> RekonDataSerializer:
    """Retrieve a indicator by id."""
    instance = await RekonData.get_or_404(pk)
    return RekonDataSerializer.read(instance)


@router.get("/", status_code=status.HTTP_200_OK)
async def listing(
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[RekonDataSerializer]:
    """Retrieve all sfd."""
    cursor = CursorInfo(request=request)

    qs = RekonData.find(**cursor.get_beanie_query_params())

    cursor.set_count(await qs.count())
    result: PaginatedData[RekonDataSerializer] = RekonDataSerializer.read_page(
        await qs.to_list(),
        request=request,
        cursor_info=cursor,
    )
    return result
