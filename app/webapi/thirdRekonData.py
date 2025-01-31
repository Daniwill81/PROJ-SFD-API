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
from app.query.thirdCrekondata import ThirdRekonQuery
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

    sfd = await Sfd.get_or_404(sfd)
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
    """Retrieve all indicator."""
    cursor = CursorInfo(request=request)
    query = ThirdRekonQuery(user=request_user, filters=request.query_params)

    if search_text := request.query_params.get("q"):
        qs = query.get_search(search_text)
    else:
        qs = query.get_qs().find(**cursor.get_beanie_query_params())

    instance_list = await qs.to_list()
    await prefetch_related(instance_list, to_attribute="sfd")

    cursor.set_count(await qs.count())
    result: PaginatedData[ThirdCRekonDataSerializer] = ThirdCRekonDataSerializer.read_page(
        instance_list,
        request=request,
        cursor_info=cursor,
    )
    return result
