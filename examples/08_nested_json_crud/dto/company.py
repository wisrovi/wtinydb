"""DTO Pydantic models for N-level nested company document."""

from pydantic import BaseModel, Field


# Level 5 Model: GeoLocation
class GeoCoordinates(BaseModel):
    """Geographic coordinates (latitude, longitude)."""

    lat: float = Field(description="Latitude value")
    lon: float = Field(description="Longitude value")


# Level 4 Model: Address
class Address(BaseModel):
    """Physical address model with embedded GeoCoordinates."""

    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    country: str = Field(description="Country name")
    geo: GeoCoordinates = Field(description="Geographic location")


# Level 3 Model: Contact & Manager
class ContactInfo(BaseModel):
    """Contact details containing nested Address."""

    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    address: Address = Field(description="Nested physical address")


class Manager(BaseModel):
    """Department manager model containing nested ContactInfo."""

    name: str = Field(description="Manager name")
    title: str = Field(description="Manager job title")
    contact: ContactInfo = Field(description="Nested contact details")


# Level 2 Model: Department
class Department(BaseModel):
    """Department model containing nested Manager."""

    name: str = Field(description="Department name")
    budget: float = Field(description="Department annual budget")
    manager: Manager = Field(description="Nested manager information")


# Level 1 Model: Company (Root Document)
class Company(BaseModel):
    """Root Company document model."""

    company_name: str = Field(description="Company full name")
    department: Department = Field(description="Nested department details")
