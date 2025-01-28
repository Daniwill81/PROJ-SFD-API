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

from sap.beanie.query import prefetch_related
from sap.fastapi.pagination import CursorInfo, PaginatedData

from app.controllers.indicator import create_c3_indicators_for_sfd, create_indicators_for_sfd
from app.models import Sfd, User
from app.models.enums import RoleEnum
from app.models.user.auth import user_auth
from app.models.utils.indicators import Indicator
from app.query.indicator import IndicatorQuery
from app.serializers.utils.indicators import IndicatorSerializer

router = APIRouter()


# Endpoint pour le calcul des indicateurs du critere 1 et 2
@router.post("/{pk}/{year}/", status_code=status.HTTP_201_CREATED)
async def create(
    pk: str,
    year: int,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> list[IndicatorSerializer]:
    """
    Create indicators for a specific SFD and year.
    Calculates ratios and marks based on available RekonData.
    """
    indicators = await create_indicators_for_sfd(sfd_id=pk, year=year)
    return [IndicatorSerializer.read(indicator) for indicator in indicators]


# Endpoint pour le calcul des indicateurs du critere 3
@router.post("/third/{pk}/{year}/", status_code=status.HTTP_201_CREATED)
async def create_third_c_indicator(
    pk: str,
    year: int,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> list[IndicatorSerializer]:
    """
    Create indicators for a specific SFD and year.
    Calculates ratios and marks based on available RekonData.
    """
    indicators = await create_c3_indicators_for_sfd(sfd_id=pk, year=year)
    return [IndicatorSerializer.read(indicator) for indicator in indicators]


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
    await prefetch_related(instance_list, to_attribute="sfd")
    await prefetch_related(instance_list, to_attribute="criteria")

    cursor.set_count(await qs.count())
    result: PaginatedData[IndicatorSerializer] = IndicatorSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result
