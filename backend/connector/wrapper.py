"""
Document generation service layer.

This module provides functions for document generation by wrapping the
functionality from docs_gen and utils modules. It serves as the business logic layer
that will later become an API.
"""

import os
from typing import Dict, Any, Optional, List, Union

# Import the functions from our modules
from backend.backend.utils import (
    load_variables,
    get_available_templates,
    create_zip_from_files,
)
from backend.backend.main import generate_document
from backend.connector.models import DocumentVariables, DocumentRequest, DocumentResponse

# Re-export utility functions directly
create_zip_from_files = create_zip_from_files
get_templates = get_available_templates

def generate_document_from_request(request: DocumentRequest) -> DocumentResponse:
    """
    Generate a single document based on a document request.
    
    Args:
        request: DocumentRequest containing template name and variables
        
    Returns:
        DocumentResponse with success status and file paths or error message
    """
    # Convert DocumentVariables to dictionary
    variables_dict = request.variables.to_dict()
    
    # Generate document
    try:
        result = generate_document(
            request.template_name, 
            variables_dict, 
            os.path.join('outputs', f"{request.template_name}.docx"),  # Let main.py handle directory creation
            generate_pdfa=request.output_format.lower() == "pdfa"
        )
        return DocumentResponse(success=True, file_paths=result)
    except Exception as e:
        return DocumentResponse(success=False, error_message=str(e))

def generate_document_from_dict(template_name: str, variables: Dict[str, Any], 
                               output_format: str = "docx", generate_all: bool = False) -> Union[DocumentResponse, List[DocumentResponse]]:
    """
    Generate one or all documents using variables.
    
    Args:
        template_name: Name of the template to use (ignored if generate_all=True)
        variables: Dictionary of template variables
        output_format: Output format ("docx" or "pdfa")
        generate_all: If True, generates all available templates instead of just one
        
    Returns:
        A single DocumentResponse or a list of DocumentResponses if generate_all=True
    """
    # Convert dict to DocumentVariables if needed
    if not isinstance(variables, DocumentVariables):
        variables_obj = DocumentVariables.from_dict(variables)
    else:
        variables_obj = variables
    
    if generate_all:
        # Get all available templates
        templates = get_templates()
        responses = []
        
        # Generate each document
        for template in templates:
            request = DocumentRequest(
                template_name=template,
                variables=variables_obj,
                output_format=output_format
            )
            response = generate_document_from_request(request)
            responses.append(response)
        
        return responses
    else:
        # Create request for a single document
        request = DocumentRequest(
            template_name=template_name,
            variables=variables_obj,
            output_format=output_format
        )
        
        # Generate document
        return generate_document_from_request(request)