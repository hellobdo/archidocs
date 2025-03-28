"""
Data models for the document generation system.

This file contains type definitions and schemas for document variables.
It serves as a single source of truth for data structures used throughout the application.
"""
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field


@dataclass
class DocumentVariables:
    """Schema for document template variables."""
    # Author information
    author_name: str
    author_name_small: str
    author_address: str
    author_nif: int
    author_registration: int
    
    # Project information
    construction_type: str
    construction_address: str
    property_description: str
    
    # Request information
    request_type: str
    requester_name: str
    requester_role: str
    requester_nif: int
    requester_address: str
    
    # Location and date
    location: str
    date: str  # Can be set to "today" to automatically use current date in format "month de year"
    
    # Land registry information
    land_registry_location: str
    land_registry_number: int
    land_registry_sublocation: str
    
    # Signature information
    signature: str
    signature_sub1: str
    signature_sub2: str
    signature_sub3: str
    
    # Regulatory references
    regulatory_reference: str
    pdm: str
    
    # Table rows (for any tabular data in templates)
    table_row1: str
    table_row2: str
    table_row3: str
    table_row4: str
    table_row5: str
    table_row6: str
    table_row7: str
    table_row8: str
    table_row9: str
    table_row10: str
    table_row11: str
    table_row12: str
    table_row13: str
    table_row14: str
    table_row15: str
    table_row16: str
    table_row17: str
    table_row18: str
    table_row19: str
    table_row20: str
    
    # Cost information
    qty: int
    cost_per_unit: int
    
    # Process information
    technical_information_id: str
    process_nr: str
    
    # Additional fields can be added as custom_fields
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for template rendering."""
        result = {}
        
        # Get all fields that aren't None
        for k, v in self.__dict__.items():
            if v is not None and k != "custom_fields":
                result[k] = v
        
        # Add custom fields if they exist
        if self.custom_fields:
            result.update(self.custom_fields)
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentVariables':
        """Create an instance from a dictionary."""
        # Extract known fields
        known_fields = {}
        custom_fields = {}
        
        # Get all field names from the class
        field_names = set(cls.__annotations__.keys())
        
        for k, v in data.items():
            if k in field_names:
                known_fields[k] = v
            else:
                custom_fields[k] = v
        
        # Create instance with known fields
        instance = cls(**known_fields)
        
        # Add custom fields
        if custom_fields:
            instance.custom_fields = custom_fields
            
        return instance


@dataclass
class DocumentRequest:
    """Request to generate a document."""
    template_name: str
    variables: DocumentVariables
    output_format: str = "docx"  # Could support other formats in the future


@dataclass
class DocumentResponse:
    """Response from document generation."""
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None 