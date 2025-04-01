from typing import TypedDict, Optional


class User(TypedDict):
    name: str
    phone: str
    birthday: str
    email: str
    username: str


class UserWithId(User):
    id: int


class PartialUser(TypedDict):
    name: Optional[int]
    phone: Optional[str]
    birthday: Optional[str]
    email: Optional[str]
    username: Optional[str]
