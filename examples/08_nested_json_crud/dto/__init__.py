"""DTO package for nested company models."""

from .company import Address, Company, ContactInfo, Department, GeoCoordinates, Manager

__all__ = ["GeoCoordinates", "Address", "ContactInfo", "Manager", "Department", "Company"]
