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

from fastapi import APIRouter, Depends, Query, Request, status

from sap.fastapi.pagination import CursorInfo, PaginatedData

from app import controllers
from app.models import Cotation, Criteria, Indicator, Sfd
from app.models.enums import RoleEnum
from app.models.user.auth import user_auth
from app.models.user.user import User
from app.serializers.criterias.cotation import CotationSerializer

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    sfd: str = Query(..., description="ID du SFD"),
    criteria: str = Query(..., description="ID du critère"),
    year: int = Query(..., description="Année de la cotation"),
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> CotationSerializer:
    """Create a cotation."""

    # Récupérer le SFD et le critère
    sfd_instance = await Sfd.get_or_404(sfd)
    criteria_instance = await Criteria.get_or_404(criteria)

    # Calculer la somme des marks des indicateurs
    total_mark = await Indicator.get_total_mark_by_sfd_criteria_and_year(
        sfd=sfd_instance.id, criteria=criteria_instance.id, year=year
    )

    # Créer une nouvelle cotation
    instance = await controllers.cotation.cotation_create(
        sfd=sfd_instance, criteria=criteria_instance, mark=total_mark, year=year
    )

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
