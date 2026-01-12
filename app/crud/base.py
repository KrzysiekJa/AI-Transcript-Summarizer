from typing import Any, Optional, List, Dict

from fastapi.encoders import jsonable_encoder
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModelException


class CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]:
    """Base class for CRUD operations."""

    def __init__(self, model: ModelType):
        """Initialize with the given model."""
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Get a single record by ID."""
        stmt = select(self.model).where(self.model.id == id)
        result = await db.exec(stmt)
        return result.first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await db.exec(stmt)
        return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        try:
            await db.commit()
            await db.refresh(db_obj)
        except SQLModelException as exc:
            await db.rollback()
            raise exc

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> ModelType:
        """Update an existing record."""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)

        try:
            await db.commit()
            await db.refresh(db_obj)
        except SQLModelException as exc:
            await db.rollback()
            raise exc

        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Remove a record by ID."""
        stmt = delete(self.model).where(self.model.id == id)

        try:
            await db.exec(stmt)
            await db.commit()
            return id
        except SQLModelException as exc:
            await db.rollback()
            raise exc
