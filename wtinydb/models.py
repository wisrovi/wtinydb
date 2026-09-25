"""WTinyDB Base Mixins and Document models."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    """Helper returning current UTC datetime."""
    return datetime.now(timezone.utc)


class TimestampMixin(BaseModel):
    """Mixin for models requiring created_at and updated_at timestamps."""

    created_at: datetime = Field(default_factory=_utc_now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=_utc_now, description="Last update timestamp")

    def touch(self) -> None:
        """Update updated_at timestamp to current UTC time."""
        self.updated_at = _utc_now()


class SoftDeleteMixin(BaseModel):
    """Mixin for models implementing logical (soft) deletion."""

    is_deleted: bool = Field(default=False, description="Flag indicating soft deletion status")
    deleted_at: Optional[datetime] = Field(default=None, description="Timestamp when deleted soft")

    def soft_delete(self) -> None:
        """Mark object as soft-deleted."""
        self.is_deleted = True
        self.deleted_at = _utc_now()

    def restore(self) -> None:
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None


class AuditMixin(TimestampMixin, SoftDeleteMixin):
    """Combined mixin providing timestamps and soft-delete audit features."""

    pass


class ForensicModel(BaseModel):
    """Base Pydantic model with forensic audit fields for WTinyDB."""

    create_by: Optional[int] = 1
    create_in: Optional[datetime] = None
    update_by: Optional[int] = None
    update_in: Optional[datetime] = None
    delete_by: Optional[int] = None
    delete_in: Optional[datetime] = None
    status: int = 1
