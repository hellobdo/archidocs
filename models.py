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
    author_name_small: Optional[str] = None
    author_address: Optional[str] = None
    author_nif: Optional[str] = None
    author_registration: Optional[str] = None
    
    # Project information
    construction_type: Optional[str] = None
    construction_address: Optional[str] = None
    property_description: Optional[str] = None
    
    # Request information
    request_type: Optional[str] = None
    requester_name: Optional[str] = None
    requester_role: Optional[str] = None
    requester_nif: Optional[str] = None
    requester_address: Optional[str] = None
    
    # Location and date
    location: Optional[str] = None
    date: Optional[str] = None  # Can be "today" for current date
    
    # Land registry information
    land_registry_location: Optional[str] = None
    land_registry_number: Optional[str] = None
    land_registry_sublocation: Optional[str] = None
    
    # Signature information
    signature: Optional[str] = None
    signature_sub1: Optional[str] = None
    signature_sub2: Optional[str] = None
    signature_sub3: Optional[str] = None
    
    # Regulatory references
    regulatory_reference: Optional[str] = None
    pdm: Optional[str] = None
    
    # Table rows (for any tabular data in templates)
    table_row1: Optional[str] = None
    table_row2: Optional[str] = None
    table_row3: Optional[str] = None
    table_row4: Optional[str] = None
    table_row5: Optional[str] = None
    table_row6: Optional[str] = None
    table_row7: Optional[str] = None
    table_row8: Optional[str] = None
    table_row9: Optional[str] = None
    table_row10: Optional[str] = None
    table_row11: Optional[str] = None
    table_row12: Optional[str] = None
    table_row13: Optional[str] = None
    table_row14: Optional[str] = None
    table_row15: Optional[str] = None
    table_row16: Optional[str] = None
    table_row17: Optional[str] = None
    table_row18: Optional[str] = None
    table_row19: Optional[str] = None
    table_row20: Optional[str] = None
    
    # Cost information
    qty: Optional[str] = None
    cost_per_unit: Optional[str] = None
    
    # Process information
    technical_information_id: Optional[str] = None
    process_nr: Optional[str] = None
    
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