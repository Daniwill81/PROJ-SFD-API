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

from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, status

from sap.beanie.query import prefetch_related
from sap.fastapi.pagination import CursorInfo, PaginatedData

from app import controllers
from app.models.enums import RoleEnum
from app.models.sfd.sfd import Sfd
from app.models.user.auth import user_auth
from app.models.user.user import User
from app.models.utils.rekonData import RekonData
from app.serializers.utils.rekonData import RekonDataSerializer

router = APIRouter()


@router.post("/upload-file/", status_code=status.HTTP_201_CREATED)
async def upload_rekon_data(
    upload_file: UploadFile,
    sfd: str = Query(..., description="ID du SFD"),
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> list[RekonDataSerializer]:
    # Vérification du type de fichier
    if not upload_file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un fichier Excel (.xlsx).")

    # Appel de la fonction de traitement des données
    saved_rekon_data = await controllers.rekonData.upload_rekonData(upload_file.file, sfd)

    # Conversion en format sérialisé
    return [RekonDataSerializer.read(instance) for instance in saved_rekon_data]


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

    instance_list = await qs.to_list()

    cursor.set_count(await qs.count())
    result: PaginatedData[RekonDataSerializer] = RekonDataSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result


@router.get("/{pk}/{year}/", status_code=status.HTTP_200_OK)
async def listing_rekondata_by_sfd_and_year(
    pk: str,
    year: int,
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[RekonDataSerializer]:
    """Récupère les RekonData par SFD et année."""
    sfd = await Sfd.get_or_404(pk)
    cursor = CursorInfo(request=request)

    # Récupération des données filtrées
    query = RekonData.find(RekonData.sfd == sfd, RekonData.year == year)
    qs = query.find(**cursor.get_beanie_query_params())

    instance_list = await qs.to_list()
    cursor.set_count(await qs.count())

    result: PaginatedData[RekonDataSerializer] = RekonDataSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result
