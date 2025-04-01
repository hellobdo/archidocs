"""
Document Generation Backend Package.

This package provides document generation functionality with a clean
service-oriented architecture that can later be exposed as an API.
"""

from backend.connector.models import DocumentVariables, DocumentRequest, DocumentResponse
from backend.connector.wrapper import (
    generate_document_from_dict,
    generate_document_from_request,
    get_templates,
)

__all__ = [
    'DocumentVariables',
    'DocumentRequest',
    'DocumentResponse',
    'generate_document_from_dict',
    'generate_document_from_request',
    'get_templates',
    'create_zip_from_files',
] 