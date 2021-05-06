from typing import Optional, Union
from enum import Enum

from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.user import UserPublic


class GenreType(str, Enum):
    action = "action"
    animation = "animation"
    comedy = "comedy"
    crime = "crime"
    drama = "drama"
    experimental = "experimental"
    fantasy = "fantasy"
    historical = "historical"
    horror = "horror"
    romance = "romance"
    science_fiction = "science_Fiction"
    thriller = "thriller"
    western = "western"
    other = "other"


class IMDBBase(CoreModel):
    """
    All common schema of our imdb database
    """
    ninetynine_popularity: Optional[float]
    movie_name: Optional[str]
    director: Optional[str]
    imdb_score: Optional[float]
    genre: Optional[GenreType] = "action"


class IMDBCreate(IMDBBase):
    movie_name: str
    director: str


class IMDBUpdate(IMDBBase):
    ninetynine_popularity: Optional[float]
    movie_name: Optional[str]
    director: Optional[str]
    imdb_score: Optional[float]
    genre: Optional[GenreType]


class IMDB(IDModelMixin, DateTimeModelMixin, IMDBBase):
    ninetynine_popularity: float
    movie_name: str
    imdb_score: float
    genre: GenreType
    created_by: int


class IMDBPublic(IMDB):
    created_by: Union[int, UserPublic]
