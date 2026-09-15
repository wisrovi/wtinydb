"""Unit tests for TimestampMixin, SoftDeleteMixin, and AuditMixin."""

from pydantic import BaseModel
from wtinydb.models import AuditMixin, SoftDeleteMixin, TimestampMixin


class SampleTimestampDoc(TimestampMixin, BaseModel):
    """Model using TimestampMixin."""

    name: str


class SampleAuditDoc(AuditMixin, BaseModel):
    """Model using AuditMixin."""

    title: str


def test_timestamp_mixin():
    """Validates default timestamp creation and touch functionality."""
    doc = SampleTimestampDoc(name="test")
    assert doc.created_at is not None
    assert doc.updated_at is not None

    initial_updated = doc.updated_at
    doc.touch()
    assert doc.updated_at >= initial_updated


def test_audit_mixin():
    """Validates soft deletion and restoration capabilities in AuditMixin."""
    doc = SampleAuditDoc(title="audit test")
    assert doc.is_deleted is False
    assert doc.deleted_at is None

    doc.soft_delete()
    assert doc.is_deleted is True
    assert doc.deleted_at is not None

    doc.restore()
    assert doc.is_deleted is False
    assert doc.deleted_at is None
