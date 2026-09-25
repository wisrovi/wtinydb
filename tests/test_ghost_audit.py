"""Unit tests for WTinyDB Enterprise Forensic Ghost Table Audit Logging functionality.

This module validates that:
1. Ghost audit log functionality can be configured.
2. Default setting disables forensic mode for 100% backward compatibility.
3. Multi-table registry tracks forensic configuration properly across models.
"""

from typing import Optional
from pydantic import BaseModel
import pytest
from wtinydb import ForensicModel, WTinyDB


class User(BaseModel):
    """Sample User model without explicit forensic base."""

    id: Optional[int] = None
    name: str
    email: str


class AuditUser(ForensicModel):
    """Sample User model deriving from ForensicModel."""

    id: Optional[int] = None
    name: str
    email: str


def test_forensic_default_disabled():
    """Verify that forensic mode is disabled by default to guarantee legacy compatibility.

    Validates that instantiated WTinyDB repository defaults forensic flag to False
    when plain BaseModel is provided without explicit forensic parameter.
    """
    repo = WTinyDB(model_class=User, in_memory=True)
    assert repo.forensic is False


def test_forensic_model_auto_enable():
    """Verify that models inheriting from ForensicModel automatically enable forensic mode.

    Validates that WTinyDB detects ForensicModel subclass and sets forensic=True
    if not explicitly overridden.
    """
    repo = WTinyDB(model_class=AuditUser, in_memory=True)
    assert repo.forensic is True


def test_multi_table_forensic_registry():
    """Verify multi-table repository propagates forensic mode setting to registered models.

    Validates that registering a ForensicModel in a multi-table WTinyDB instance
    maintains individual model forensic settings.
    """
    app = WTinyDB(models=[User, AuditUser], in_memory=True)
    assert app["user"].forensic is False
    assert app["audituser"].forensic is True
