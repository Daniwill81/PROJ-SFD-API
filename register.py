"""
Register metadata to run the Application.

Data is loading from metadata.yaml
"""
import asyncio
import typing

import yaml

from sap.beanie import Document
from sap.beanie.exceptions import Object404Error

from app.models import RoleDesc, User
from app.models.enums import RoleEnum, RoleTypeEnum
from AppMain.asgi import initialize_beanie
from AppMain.settings import logger  # AppSettings


async def register() -> None:
    """Initialize the database with default data."""
    await initialize_beanie()

    with open("metadata.yml", "r", encoding="utf-8") as stream:
        metadata: dict[str, typing.Any] = yaml.safe_load(stream)

    await register_roledescs(metadata["rolesdesc"])
    await register_superusers(data_list=metadata["superusers"])


async def register_data(doc_model: type[Document], data_list: list[dict[str, typing.Any]], pk_name: str) -> None:
    """Populate database with default data."""
    for data_row in data_list:
        logger.debug("Loading data for %s: %s", doc_model.__name__, data_row[pk_name])
        try:
            instance = await doc_model.find_one_or_404(getattr(doc_model, pk_name) == data_row[pk_name])
        except Object404Error:
            await doc_model(**data_row).create()
        else:
            instance = instance.model_copy(update=data_row)
            await instance.save()


async def register_roledescs(data_list: list[dict[str, typing.Any]]) -> None:
    """Register roles described in metadata."""
    await register_data(RoleDesc, data_list, "type")


async def register_superusers(data_list: list[dict[str, typing.Any]]) -> None:
    """Create the super admin account."""
    user_role: RoleDesc = await RoleDesc.find_one_or_404(RoleDesc.type == RoleTypeEnum.ADMIN)

    for data_row in data_list:
        user = await User.find_one(User.email == data_row["email"])
        if user:
            print(f"Admin {user.email} already exists.")
            continue

        user = await User(
            first_name=data_row["first_name"],
            last_name=data_row["last_name"],
            email=data_row["email"],
            password=data_row["password"],
            role=RoleEnum.ADMIN1,
            roledesc=user_role,
        ).create()

        assert user.id
        print(f"Admin {user.email} was successfully created.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(register())
