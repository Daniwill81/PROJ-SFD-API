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
from app.models.sfd.sfd import Sfd
from app.models.utils.rekonData import RekonData
from app.serializers.utils.rekonData import RekonDataSerializer

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    rekon_data_list: list[RekonData],
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> list[RekonDataSerializer]:
    """Create multiple rekonData."""
    sfd = await Sfd.get_or_404(rekon_data_list[0].sfd)
    
    created_rekon_data = await controllers.rekonData.rekonData_create(
        rekon_data_list=[{
            'account_number': data.account_number,
            'amount': data.amount,
            'year': data.year,
            'indicator': data.indicator,
            'criteria_id': data.criteria,
        } for data in rekon_data_list],
        sfd=sfd
    )

    return [RekonDataSerializer.read(instance) for instance in created_rekon_data]


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
