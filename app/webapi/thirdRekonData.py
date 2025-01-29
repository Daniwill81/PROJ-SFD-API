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
from app.models.utils.thirdCriRekonData import ThirdCrekonData
from app.serializers.utils.thirdCriRekonData import ThirdCRekonDataSerializer

router = APIRouter()


@router.post("/upload-file/", status_code=status.HTTP_201_CREATED)
async def upload_third_crekondata_file(
    upload_file: UploadFile,
    sfd: str = Query(..., description="ID du SFD"),
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> list[ThirdCRekonDataSerializer]:
    # Vérification du type de fichier
    if not upload_file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un fichier Excel (.xlsx).")

    # Appel de la fonction de traitement des données
    saved_rekon_data = await controllers.rekonData.upload_third_crekondata_file(upload_file.file, sfd)

    # Conversion en format sérialisé
    return [ThirdCRekonDataSerializer.read(instance) for instance in saved_rekon_data]


@router.get("/{pk}/", status_code=status.HTTP_200_OK)
async def retrieve(
    pk: str,
) -> ThirdCRekonDataSerializer:
    """Retrieve a indicator by id."""
    instance = await ThirdCrekonData.get_or_404(pk)
    return ThirdCRekonDataSerializer.read(instance)


@router.get("/", status_code=status.HTTP_200_OK)
async def listing(
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[ThirdCRekonDataSerializer]:
    """Retrieve all sfd."""
    cursor = CursorInfo(request=request)

    qs = ThirdCrekonData.find(**cursor.get_beanie_query_params())

    instance_list = await qs.to_list()

    cursor.set_count(await qs.count())
    result: PaginatedData[ThirdCRekonDataSerializer] = ThirdCRekonDataSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result


@router.get("/{pk}/{year}/", status_code=status.HTTP_200_OK)
async def get_thirdcrekondata_by_sfd_and_year(
    pk: str,
    year: int,
    request: Request,
    request_user: User = Depends(user_auth.require(RoleEnum.get_list_primary())),
) -> PaginatedData[ThirdCRekonDataSerializer]:
    """Récupère les ThirdCrekonData par SFD et année."""
    sfd = Sfd.get_or_404(pk)
    cursor = CursorInfo(request=request)

    # Récupération des données filtrées
    query = ThirdCrekonData.find(ThirdCrekonData.sfd == sfd, ThirdCrekonData.year == year)
    qs = query.find(**cursor.get_beanie_query_params())

    instance_list = await qs.to_list()
    cursor.set_count(await qs.count())

    result: PaginatedData[ThirdCRekonDataSerializer] = ThirdCRekonDataSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result
