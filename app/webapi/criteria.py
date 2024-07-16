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

from app.models.criterias.criteria import Criteria
from app.models.enums import RoleEnum
from app.models.user.auth import user_auth
from app.models.user.user import User
from app.serializers.criterias.criteria import CriteriaSerializer, WriteCriteriaSerializer

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    request: Request,
    serializer_write: WriteCriteriaSerializer,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> CriteriaSerializer:
    """Create a criteria."""
    await serializer_write.run_async_validators(request=request)
    instance = await serializer_write.create(request=request, request_user=request_user)
    return CriteriaSerializer.read(instance)


@router.get("/{pk}/", status_code=status.HTTP_200_OK)
async def retrieve(
    pk: str,
) -> CriteriaSerializer:
    """Retrieve a criteria by id."""
    instance = await Criteria.get_or_404(pk)
    return CriteriaSerializer.read(instance)


@router.get("/", status_code=status.HTTP_200_OK)
async def listing(
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[CriteriaSerializer]:
    """Retrieve all criteria."""
    cursor = CursorInfo(request=request)

    qs = Criteria.find(**cursor.get_beanie_query_params())

    cursor.set_count(await qs.count())
    result: PaginatedData[CriteriaSerializer] = CriteriaSerializer.read_page(
        await qs.to_list(),
        request=request,
        cursor_info=cursor,
    )
    return result
