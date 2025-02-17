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

from sap.beanie.query import prefetch_related
from sap.fastapi.pagination import CursorInfo, PaginatedData

from app import controllers
from app.models import GlobalNote, Sfd, User
from app.models.enums import RoleEnum
from app.models.user.auth import user_auth
from app.query.global_note import GlobalNoteQuery
from app.serializers.criterias.global_note import GlobalNoteSerializer

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_global_note(
    sfd: str = Query(..., description="ID du SFD"),
    year: int = Query(..., description="Année de l'evaluation de risque"),
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> GlobalNoteSerializer:
    """Create a global note for the given SFD and year."""

    # Récupérer le SFD
    sfd_instance = await Sfd.get_or_404(sfd)

    # Calculer la note globale
    instance = await controllers.global_note.global_note_calcul(sfd=sfd_instance, year=year)

    return GlobalNoteSerializer.read(instance)


@router.get("/{pk}/", status_code=status.HTTP_200_OK)
async def retrieve(
    pk: str,
) -> GlobalNoteSerializer:
    """Retrieve a criteria by id."""
    instance = await GlobalNote.get_or_404(pk)
    return GlobalNoteSerializer.read(instance)


@router.get("/", status_code=status.HTTP_200_OK)
async def listing(
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[GlobalNoteSerializer]:
    """Retrieve all indicator."""
    cursor = CursorInfo(request=request)
    query = GlobalNoteQuery(user=request_user, filters=request.query_params)

    if search_text := request.query_params.get("q"):
        qs = query.get_search(search_text)
    else:
        qs = query.get_qs().find(**cursor.get_beanie_query_params())

    instance_list = await qs.to_list()
    await prefetch_related(instance_list, to_attribute="sfd")

    cursor.set_count(await qs.count())
    result: PaginatedData[GlobalNoteSerializer] = GlobalNoteSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result
