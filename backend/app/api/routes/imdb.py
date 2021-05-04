from typing import List

from fastapi import APIRouter, Body, Depends, status

from app.models.user import UserInDB
from app.models.imdb import IMDBCreate, IMDBUpdate, IMDB, IMDBPublic

from app.db.repositories.imdb import IMDBRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.imdb import get_imdb_by_id_from_path, check_imdb_modification_permissions


router = APIRouter()


@router.post("/", response_model=IMDBPublic, name="imdb:create-imdb", status_code=status.HTTP_201_CREATED)
async def create_new_imdb(
    new_imdb: IMDBCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    imdb_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> IMDBPublic:
    return await imdb_repo.create_imdb(new_imdb=new_imdb, requesting_user=current_user)


@router.get("/", response_model=List[IMDBPublic], name="imdb:list-all-user-imdb")
async def list_all_user_imdbs(
    current_user: UserInDB = Depends(get_current_active_user),
    imdb_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> List[IMDBPublic]:
    return await imdb_repo.list_all_user_imdbs(requesting_user=current_user)


@router.get("/{imdb_id}/", response_model=IMDBPublic, name="imdb:get-imdb-by-id")
async def get_imdb_by_id(imdb: IMDB = Depends(get_imdb_by_id_from_path)) -> IMDBPublic:
    return imdb


@router.put(
    "/{imdb_id}/",
    response_model=IMDBPublic,
    name="imdb:update-imdb-by-id",
    dependencies=[Depends(check_imdb_modification_permissions)],
)
async def update_imdb_by_id(
    imdb: IMDB = Depends(get_imdb_by_id_from_path),
    imdb_update: IMDBUpdate = Body(..., embed=True),
    imdb_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> IMDBPublic:
    return await imdb_repo.update_imdb(imdb=imdb, imdb_update=imdb_update)


@router.delete(
    "/{imdb_id}/",
    response_model=int,
    name="imdb:delete-imdb-by-id",
    dependencies=[Depends(check_imdb_modification_permissions)],
)
async def delete_imdb_by_id(
    imdb: IMDB = Depends(get_imdb_by_id_from_path),
    imdb_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> int:
    return await imdb_repo.delete_imdb_by_id(imdb=imdb)

