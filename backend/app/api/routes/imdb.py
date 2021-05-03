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
async def create_new_cleaning(
    new_cleaning: IMDBCreate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> IMDBPublic:
    return await cleanings_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=current_user)


@router.get("/", response_model=List[IMDBPublic], name="imdb:list-all-user-imdb")
async def list_all_user_cleanings(
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> List[IMDBPublic]:
    return await cleanings_repo.list_all_user_cleanings(requesting_user=current_user)


@router.get("/{cleaning_id}/", response_model=IMDBPublic, name="imdb:get-cleaning-by-id")
async def get_cleaning_by_id(cleaning: IMDB = Depends(get_imdb_by_id_from_path)) -> IMDBPublic:
    return cleaning


@router.put(
    "/{cleaning_id}/",
    response_model=IMDBPublic,
    name="imdb:update-cleaning-by-id",
    dependencies=[Depends(check_imdb_modification_permissions)],
)
async def update_cleaning_by_id(
    cleaning: IMDB = Depends(get_imdb_by_id_from_path),
    cleaning_update: IMDBUpdate = Body(..., embed=True),
    cleanings_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> IMDBPublic:
    return await cleanings_repo.update_cleaning(cleaning=cleaning, cleaning_update=cleaning_update)


@router.delete(
    "/{cleaning_id}/",
    response_model=int,
    name="imdb:delete-cleaning-by-id",
    dependencies=[Depends(check_imdb_modification_permissions)],
)
async def delete_cleaning_by_id(
    cleaning: IMDB = Depends(get_imdb_by_id_from_path),
    cleanings_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> int:
    return await cleanings_repo.delete_cleaning_by_id(cleaning=cleaning)

