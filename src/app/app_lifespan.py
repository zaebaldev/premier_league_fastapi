from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown
    await db_helper.dispose()
