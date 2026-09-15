from pydantic import BaseModel, Field


class User(BaseModel):
    """User document model for basic CRUD operations."""

    name: str = Field(description="Full user name")
    email: str = Field(description="Email address")
    age: int = Field(default=18, description="Age in years")
