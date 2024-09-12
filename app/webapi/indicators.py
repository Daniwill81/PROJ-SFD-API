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
from app.models.utils.indicators import Indicator
from app.query.indicator import IndicatorQuery
from app.serializers.utils.indicators import IndicatorSerializer

router = APIRouter()


@router.get("/{pk}/", status_code=status.HTTP_200_OK)
async def retrieve(
    pk: str,
) -> IndicatorSerializer:
    """Retrieve a indicator by id."""
    instance = await Indicator.get_or_404(pk)
    return IndicatorSerializer.read(instance)


@router.get("/", status_code=status.HTTP_200_OK)
async def listing(
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[IndicatorSerializer]:
    """Retrieve all indicator."""
    cursor = CursorInfo(request=request)
    query = IndicatorQuery(user=request_user, filters=request.query_params)

    if search_text := request.query_params.get("q"):
        qs = query.get_search(search_text)
    else:
        qs = query.get_qs().find(**cursor.get_beanie_query_params())

    instance_list = await qs.to_list()

    cursor.set_count(await qs.count())
    result: PaginatedData[IndicatorSerializer] = IndicatorSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result
