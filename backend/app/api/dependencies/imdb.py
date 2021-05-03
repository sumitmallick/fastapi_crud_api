from fastapi import HTTPException, Depends, Path, status

from app.models.user import UserInDB
from app.models.imdb import IMDBPublic
from app.db.repositories.imdb import IMDBRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user


async def get_imdb_by_id_from_path(
    imdb_id: int = Path(..., ge=1),
    current_user: UserInDB = Depends(get_current_active_user),
    imdb_repo: IMDBRepository = Depends(get_repository(IMDBRepository)),
) -> IMDBPublic:
    imdb = await imdb_repo.get_imdb_by_id(id=imdb_id, requesting_user=current_user)

    if not imdb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No imdb movie found with that id.",
        )

    return imdb


def check_imdb_modification_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    imdb: IMDBPublic = Depends(get_imdb_by_id_from_path),
) -> None:
    if not user_owns_imdb(user=current_user, imdb=imdb):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Users are only able to modify cleanings that they created.",
        )


def user_owns_imdb(*, user: UserInDB, imdb: IMDBPublic) -> bool:
    if isinstance(imdb.owner, int):
        return imdb.owner == user.id

    return imdb.owner.id == user.id
