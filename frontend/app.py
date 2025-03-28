"""
Document Generation System - Streamlit UI

This file contains the Streamlit user interface for the document generation system.
It uses the backend service layer for all document processing functionality.
"""
import os
import json
import streamlit as st
from datetime import datetime
import sys

# Add parent directory to sys.path to make backend imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend functionality
from backend import (
    DocumentVariables,
    DocumentRequest,
    DocumentResponse,
    generate_document_from_dict,
    generate_document_from_request,
    load_and_generate_document,
    get_templates
)


def load_default_variables():
    """Load default variables from the JSON file."""
    try:
        with open('backend/templates/variables.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Variables file not found. Please create 'backend/templates/variables.json'.")
        return {}


def display_document_form(default_values=None):
    """Display a form for editing document variables."""
    if default_values is None:
        default_values = {}
    
    # Create sections with expanders to organize fields
    with st.expander("Informações do Autor", expanded=True):
        author_name = st.text_input("Nome do Autor", value=default_values.get("author_name", ""))
        author_address = st.text_input("Endereço do Autor", value=default_values.get("author_address", ""))
        author_nif = st.text_input("NIF do Autor", value=default_values.get("author_nif", ""))
        author_registration = st.text_input("Registro do Autor", value=default_values.get("author_registration", ""))
    
    with st.expander("Informações do Projeto", expanded=True):
        construction_type = st.text_input("Tipo de Construção", value=default_values.get("construction_type", ""))
        construction_address = st.text_input("Endereço do Projeto", value=default_values.get("construction_address", ""))
        property_description = st.text_area("Descrição da Propriedade", value=default_values.get("property_description", ""))
    
    with st.expander("Informações da Solicitação", expanded=False):
        request_type = st.text_input("Tipo de Solicitação", value=default_values.get("request_type", ""))
        requester_name = st.text_input("Nome do Solicitante", value=default_values.get("requester_name", ""))
        requester_role = st.text_input("Cargo do Solicitante", value=default_values.get("requester_role", ""))
        requester_nif = st.text_input("NIF do Solicitante", value=default_values.get("requester_nif", ""))
        requester_address = st.text_input("Endereço do Solicitante", value=default_values.get("requester_address", ""))
    
    with st.expander("Location and Date", expanded=False):
        location = st.text_input("Localização", value=default_values.get("location", ""))
        date = st.text_input("Data (use 'today' para data atual)", value=default_values.get("date", "today"))
    
    with st.expander("Informações do Registo de Imóveis", expanded=False):
        land_registry_location = st.text_input("Localização do Registo de Imóveis", value=default_values.get("land_registry_location", ""))
        land_registry_number = st.text_input("Número do Registo de Imóveis", value=default_values.get("land_registry_number", ""))
        land_registry_sublocation = st.text_input("Freguesia", value=default_values.get("land_registry_sublocation", ""))
    
    with st.expander("Assinatura", expanded=False):
        signature = st.text_input("Assinatura", value=default_values.get("signature", ""))
        signature_sub1 = st.text_input("Signature Sub 1", value=default_values.get("signature_sub1", ""))
        signature_sub2 = st.text_input("Signature Sub 2", value=default_values.get("signature_sub2", ""))
        signature_sub3 = st.text_input("Signature Sub 3", value=default_values.get("signature_sub3", ""))
    
    with st.expander("Referências Regulatórias", expanded=False):
        regulatory_reference = st.text_input("Referência Regulatória", value=default_values.get("regulatory_reference", ""))
        pdm = st.text_input("PDM", value=default_values.get("pdm", ""))
    
    with st.expander("Custo", expanded=True):
        qty = st.number_input("Quantidade em m2", value=float(default_values.get("qty", 0)), format="%.2f")
        cost_per_unit = st.number_input("Custo por Unidade", value=float(default_values.get("cost_per_unit", 0)), format="%.2f")
    
    with st.expander("Informações do Processo", expanded=False):
        technical_information_id = st.text_input("ID da Informação Técnica", value=default_values.get("technical_information_id", ""))
        process_nr = st.text_input("Número do Processo", value=default_values.get("process_nr", ""))
    
    # Build variables dictionary
    variables = {
        "author_name": author_name,
        "author_name_small": author_name_small,
        "author_address": author_address,
        "author_nif": author_nif,
        "author_registration": author_registration,
        "construction_type": construction_type,
        "construction_address": construction_address,
        "property_description": property_description,
        "request_type": request_type,
        "requester_name": requester_name,
        "requester_role": requester_role,
        "requester_nif": requester_nif,
        "requester_address": requester_address,
        "location": location,
        "date": date,
        "land_registry_location": land_registry_location,
        "land_registry_number": land_registry_number,
        "land_registry_sublocation": land_registry_sublocation,
        "signature": signature,
        "signature_sub1": signature_sub1,
        "signature_sub2": signature_sub2,
        "signature_sub3": signature_sub3,
        "regulatory_reference": regulatory_reference,
        "pdm": pdm,
        "qty": str(qty),
        "cost_per_unit": str(cost_per_unit),
        "technical_information_id": technical_information_id,
        "process_nr": process_nr
    }
    
    # Remove empty fields
    variables = {k: v for k, v in variables.items() if v}
    
    return variables


def save_variables(variables):
    """Save the variables to a JSON file."""
    backup_path = "backend/templates/variables_backup.json"
    
    # Create backup of original file if it exists
    if os.path.exists("backend/templates/variables.json"):
        with open("backend/templates/variables.json", 'r', encoding='utf-8') as f:
            original = json.load(f)
            
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(original, f, indent=2, ensure_ascii=False)
        
        st.success(f"Created backup at {backup_path}")
    
    # Save new variables
    with open("backend/templates/variables.json", 'w', encoding='utf-8') as f:
        json.dump(variables, f, indent=2, ensure_ascii=False)
    
    st.success("Variables saved successfully!")


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Document Generator",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("Document Generator")
    st.write("Generate professional documents from templates")
    
    # Get available templates
    try:
        template_list = get_templates()
        if not template_list:
            st.warning("No templates found. Please add templates to the 'backend/templates/files' directory.")
    except Exception as e:
        st.error(f"Error loading templates: {str(e)}")
        template_list = []
    
    # Sidebar for actions and template selection
    with st.sidebar:
        st.header("Controls")
        
        # Load/save variables
        if st.button("Load Default Variables"):
            st.session_state.variables = load_default_variables()
            st.success("Variables loaded!")
            
        if st.button("Save Variables"):
            if "variables" in st.session_state:
                save_variables(st.session_state.variables)
            else:
                st.error("No variables to save.")
        
        # Template selection
        st.header("Generate Documents")
        if template_list:
            selected_template = st.selectbox(
                "Select template",
                options=template_list
            )
            
            # Generate buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate Selected"):
                    if "variables" in st.session_state:
                        with st.spinner("Generating document..."):
                            result = generate_document_from_dict(
                                selected_template,
                                st.session_state.variables
                            )
                            if result.success:
                                st.success(f"Document generated: {result.file_path}")
                                # Create download link
                                with open(result.file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Document",
                                        data=file,
                                        file_name=os.path.basename(result.file_path),
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                            else:
                                st.error(f"Error: {result.error_message}")
                    else:
                        st.error("Please fill in the form first.")
            
            with col2:
                if st.button("Generate All"):
                    if "variables" in st.session_state:
                        with st.spinner("Generating all documents..."):
                            results = generate_document_from_dict(
                                selected_template,
                                st.session_state.variables,
                                generate_all=True
                            )
                            success_count = sum(1 for r in results if r.success)
                            if success_count > 0:
                                st.success(f"Generated {success_count} documents successfully!")
                                # List the files
                                st.write("Generated documents:")
                                for result in results:
                                    if result.success:
                                        st.write(f"- {os.path.basename(result.file_path)}")
                            else:
                                st.error("Failed to generate any documents.")
                    else:
                        st.error("Please fill in the form first.")
    
    # Main form area
    if "variables" not in st.session_state:
        st.session_state.variables = load_default_variables()
    
    st.header("Document Variables")
    updated_variables = display_document_form(st.session_state.variables)
    
    # Update session state when form is submitted
    if st.button("Update Variables"):
        st.session_state.variables = updated_variables
        st.success("Variables updated!")


if __name__ == "__main__":
    main() 