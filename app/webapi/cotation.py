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
from app.models import Cotation
from app.models.enums import RoleEnum
from app.models.user.auth import user_auth
from app.models.user.user import User
from app.serializers.criterias.cotation import CotationSerializer

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    cotation: Cotation,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> CotationSerializer:
    """Create a indicator."""
    sfd = cotation.sfd
    criteria = cotation.criteria
    mark = cotation.mark
    year = cotation.year

    await controllers.cotation.cotation_create(sfd=sfd, criteria=criteria, mark=mark, year=year)
    instance = cotation

    return CotationSerializer.read(instance)


@router.get("/{pk}/", status_code=status.HTTP_200_OK)
async def retrieve(
    pk: str,
) -> CotationSerializer:
    """Retrieve a criteria by id."""
    instance = await Cotation.get_or_404(pk)
    return CotationSerializer.read(instance)


@router.get("/", status_code=status.HTTP_200_OK)
async def listing(
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[CotationSerializer]:
    """Retrieve all criteria."""
    cursor = CursorInfo(request=request)

    qs = Cotation.find(**cursor.get_beanie_query_params())

    cursor.set_count(await qs.count())
    result: PaginatedData[CotationSerializer] = CotationSerializer.read_page(
        await qs.to_list(),
        request=request,
        cursor_info=cursor,
    )
    return result
