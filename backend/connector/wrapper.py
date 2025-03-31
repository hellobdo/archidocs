"""
Document generation service layer.

This module provides functions for document generation by wrapping the
functionality from generate_docx.py. It serves as the business logic layer
that will later become an API.
"""

import os
import zipfile
from typing import Dict, Any, Optional, List, Union
# Import the functions from the original generate_docx.py
from backend.generate_docx import (
    load_variables,
    get_available_templates,
    generate_document,
)
from backend.connector.models import DocumentVariables, DocumentRequest, DocumentResponse

def get_templates() -> List[str]:
    """
    Get a list of available document templates.
    
    Returns:
        List of template names without file extensions
    """
    return get_available_templates()


def generate_document_from_request(request: DocumentRequest) -> DocumentResponse:
    """
    Generate a single document based on a document request.
    
    Args:
        request: DocumentRequest containing template name and variables
        
    Returns:
        DocumentResponse with success status and file path or error message
    """
    # Convert DocumentVariables to dictionary
    variables_dict = request.variables.to_dict()
    
    # Set up output path
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    output_path = os.path.join('outputs', f"{request.template_name}.{request.output_format}")
    
    # Generate document
    try:
        success = generate_document(request.template_name, variables_dict, output_path)
        if success:
            return DocumentResponse(success=True, file_path=output_path)
        else:
            return DocumentResponse(success=False, error_message=f"Failed to generate document using template {request.template_name}")
    except Exception as e:
        return DocumentResponse(success=False, error_message=str(e))


def generate_document_from_dict(template_name: str, variables: Dict[str, Any], 
                               output_format: str = "docx", generate_all: bool = False) -> Union[DocumentResponse, List[DocumentResponse]]:
    """
    Generate one or all documents using variables.
    
    Args:
        template_name: Name of the template to use (ignored if generate_all=True)
        variables: Dictionary of template variables
        output_format: Output format (default: docx)
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


def load_and_generate_document(template_name: str, variables_path: str = "templates/variables.json", 
                              output_format: str = "docx", generate_all: bool = False) -> Union[DocumentResponse, List[DocumentResponse]]:
    """
    Load variables from a JSON file and generate one or all documents.
    
    Args:
        template_name: Name of the template to use (ignored if generate_all=True)
        variables_path: Path to the variables JSON file
        output_format: Output format (default: docx)
        generate_all: If True, generates all available templates instead of just one
        
    Returns:
        A single DocumentResponse or a list of DocumentResponses if generate_all=True
    """
    try:
        # Load variables from file
        variables_dict = load_variables(variables_path)
        
        # Generate document(s)
        return generate_document_from_dict(template_name, variables_dict, output_format, generate_all)
    except Exception as e:
        return DocumentResponse(success=False, error_message=str(e))

def create_zip_from_files(files: List[str], output_zip_path: str) -> Optional[str]:
    """
    Create a ZIP file from a list of files.
    
    Args:
        files: List of file paths to include in the ZIP
        output_zip_path: Path where the ZIP file should be saved
    
    Returns:
        Path to the created ZIP file or None if creation failed
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_zip_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Check that all files exist
        valid_files = []
        for file_path in files:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                valid_files.append(file_path)
            else:
                print(f"Warning: File not found or empty: {file_path}")
        
        # If no valid files, return None
        if not valid_files:
            print("No valid files to add to ZIP")
            return None
        
        # Create the ZIP file
        with zipfile.ZipFile(output_zip_path, 'w') as zip_file:
            for file_path in valid_files:
                file_name = os.path.basename(file_path)
                print(f"Adding to ZIP: {file_path} as {file_name}")
                zip_file.write(file_path, arcname=file_name)
        
        # Verify the ZIP was created
        if os.path.exists(output_zip_path) and os.path.getsize(output_zip_path) > 0:
            print(f"ZIP created successfully at {output_zip_path} with size {os.path.getsize(output_zip_path)} bytes")
            return output_zip_path
        else:
            print(f"ZIP creation failed: {output_zip_path}")
            return None
            
    except Exception as e:
        print(f"Error creating ZIP: {str(e)}")
        import traceback
        traceback.print_exc()
        return None