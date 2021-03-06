from typing import List, Union

from fastapi import HTTPException, status

from databases import Database

from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository

from app.models.imdb import IMDBCreate, IMDBUpdate, IMDB, IMDBPublic
from app.models.user import UserInDB


CREATE_IMDB_QUERY = """
    INSERT INTO imdb (ninetynine_popularity, movie_name, imdb_score, genre, director, created_by)
    VALUES (:ninetynine_popularity, :movie_name, :imdb_score, :genre, :director, :created_by)
    RETURNING id, ninetynine_popularity, movie_name, imdb_score, genre, director, created_by, created_at, updated_at;
"""

GET_IMDB_BY_ID_QUERY = """
    SELECT id, ninetynine_popularity, movie_name, imdb_score, genre, director, created_by, created_at, updated_at
    FROM imdb
    WHERE id = :id;
"""

LIST_ALL_USER_IMDBS_QUERY = """
    SELECT id, ninetynine_popularity, movie_name, imdb_score, genre, director, created_by, created_at, updated_at
    FROM imdb
    WHERE created_by = :created_by;
"""

UPDATE_IMDB_BY_ID_QUERY = """
    UPDATE imdb
    SET imdb_score = :imdb_score,
        ninetynine_popularity = :ninetynine_popularity,
        movie_name = :movie_name,
        director = :director,
        genre = :genre
    WHERE id = :id
    RETURNING id, ninetynine_popularity, movie_name, imdb_score, genre, director, created_by, created_at, updated_at;
"""

DELETE_IMDB_BY_ID_QUERY = """
    DELETE FROM imdb
    WHERE id = :id
    RETURNING id;
"""


class IMDBRepository(BaseRepository):
    """
    All database actions associated with the imdb resource
    """

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.users_repo = UsersRepository(db)

    async def create_imdb(self, *, new_imdb: IMDBCreate, requesting_user: UserInDB) -> IMDB:
        imdb = await self.db.fetch_one(
            query=CREATE_IMDB_QUERY, values={**new_imdb.dict(), "created_by": requesting_user.id}
        )
        return IMDB(**imdb)

    async def get_imdb_by_id(
        self, *, id: int, requesting_user: UserInDB, populate: bool = True
    ) -> Union[IMDB, IMDBPublic]:
        imdb_record = await self.db.fetch_one(query=GET_IMDB_BY_ID_QUERY, values={"id": id})

        if imdb_record:
            imdb = IMDB(**imdb_record)

            if populate:
                return await self.populate_imdb(imdb=imdb, requesting_user=requesting_user)

            return imdb

    async def list_all_user_imdbs(self, requesting_user: UserInDB) -> List[IMDB]:
        imdb_records = await self.db.fetch_all(
            query=LIST_ALL_USER_IMDBS_QUERY, values={"created_by": requesting_user.id}
        )

        return [IMDB(**l) for l in imdb_records]

    async def update_imdb(self, *, imdb: IMDB, imdb_update: IMDBUpdate) -> IMDB:
        imdb_update_params = imdb.copy(update=imdb_update.dict(exclude_unset=True))
        if imdb_update_params.imdb_score is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid imdb type. Cannot be None."
            )

        updated_imdb = await self.db.fetch_one(
            query=UPDATE_IMDB_BY_ID_QUERY,
            values=imdb_update_params.dict(exclude={"created_by", "created_at", "updated_at"}),
        )
        return IMDB(**updated_imdb)

    async def delete_imdb_by_id(self, *, imdb: IMDB) -> int:
        return await self.db.execute(query=DELETE_IMDB_BY_ID_QUERY, values={"id": imdb.id})

    async def populate_imdb(self, *, imdb: IMDB, requesting_user: UserInDB = None) -> IMDBPublic:
        return IMDBPublic(
            **imdb.dict(exclude={"created_by"}),
            created_by=await self.users_repo.get_user_by_id(user_id=imdb.created_by),
            # any other populated fields for imdb public would be tacked on here
        )

