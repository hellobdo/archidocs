"""
Document Generation Backend Package.

This package provides document generation functionality with a clean
service-oriented architecture that can later be exposed as an API.
"""

from backend.models import DocumentVariables, DocumentRequest, DocumentResponse
from backend.wrapper import (
    generate_document_from_dict,
    generate_document_from_request,
    load_and_generate_document,
    get_templates,
    convert_to_pdfa,
    create_zip_from_files
)

__all__ = [
    'DocumentVariables',
    'DocumentRequest',
    'DocumentResponse',
    'generate_document_from_dict',
    'generate_document_from_request',
    'load_and_generate_document',
    'get_templates',
    'convert_to_pdfa',
    'create_zip_from_files'
] 