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
    
    with st.expander("Informações do Solicitante", expanded=False):
        requester_name = st.text_input("Nome do Solicitante", value=default_values.get("requester_name", ""))
        requester_role = st.text_input("Cargo do Solicitante", value=default_values.get("requester_role", ""))
        requester_nif = st.text_input("NIF do Solicitante", value=default_values.get("requester_nif", ""))
        requester_address = st.text_input("Endereço do Solicitante", value=default_values.get("requester_address", ""))

    with st.expander("Informações do Projeto", expanded=False):
        construction_type = st.text_input("Tipo de Construção", value=default_values.get("construction_type", ""))
        construction_address = st.text_input("Endereço do Projeto", value=default_values.get("construction_address", ""))
        property_description = st.text_area("Descrição da Propriedade", value=default_values.get("property_description", ""))
        request_type = st.text_input("Tipo de Solicitação", value=default_values.get("request_type", ""))
        qty = st.number_input("Quantidade em m2", value=float(default_values.get("qty", 0)), format="%.2f")
        cost_per_unit = st.number_input("Custo por m2", value=float(default_values.get("cost_per_unit", 0)), format="%.2f")
        
    
    with st.expander("Informações do Registo de Imóveis", expanded=False):
        land_registry_location = st.text_input("Localização no Registo de Imóveis", value=default_values.get("land_registry_location", ""))
        land_registry_number = st.text_input("Número no Registo de Imóveis", value=default_values.get("land_registry_number", ""))
        land_registry_sublocation = st.text_input("Freguesia", value=default_values.get("land_registry_sublocation", ""))
    
    with st.expander("Referências Regulatórias", expanded=False):
        regulatory_reference = st.text_input("Referência Regulatória", value=default_values.get("regulatory_reference", ""))
        pdm = st.text_input("PDM", value=default_values.get("pdm", ""))
        technical_information_id = st.text_input("ID da Informação Técnica", value=default_values.get("technical_information_id", ""))
        process_nr = st.text_input("Número do Processo", value=default_values.get("process_nr", ""))

    with st.expander("Tabelas opcionais", expanded=False):
        table_row1 = st.text_input("Linha 1", value=default_values.get("table_row1", ""))
        table_row2 = st.text_input("Linha 2", value=default_values.get("table_row2", ""))
        table_row3 = st.text_input("Linha 3", value=default_values.get("table_row3", ""))
        table_row4 = st.text_input("Linha 4", value=default_values.get("table_row4", ""))
        table_row5 = st.text_input("Linha 5", value=default_values.get("table_row5", ""))
        table_row6 = st.text_input("Linha 6", value=default_values.get("table_row6", ""))
        table_row7 = st.text_input("Linha 7", value=default_values.get("table_row7", ""))
        table_row8 = st.text_input("Linha 8", value=default_values.get("table_row8", ""))
        table_row9 = st.text_input("Linha 9", value=default_values.get("table_row9", ""))
        table_row10 = st.text_input("Linha 10", value=default_values.get("table_row10", ""))
        table_row11 = st.text_input("Linha 11", value=default_values.get("table_row11", ""))
        table_row12 = st.text_input("Linha 12", value=default_values.get("table_row12", ""))
        table_row13 = st.text_input("Linha 13", value=default_values.get("table_row13", ""))
        table_row14 = st.text_input("Linha 14", value=default_values.get("table_row14", ""))
        table_row15 = st.text_input("Linha 15", value=default_values.get("table_row15", ""))
        table_row16 = st.text_input("Linha 16", value=default_values.get("table_row16", ""))
        table_row17 = st.text_input("Linha 17", value=default_values.get("table_row17", ""))
        table_row18 = st.text_input("Linha 18", value=default_values.get("table_row18", ""))
        table_row19 = st.text_input("Linha 19", value=default_values.get("table_row19", ""))
        table_row20 = st.text_input("Linha 20", value=default_values.get("table_row20", ""))


    with st.expander("Informações do Autor", expanded=False):
        author_name = st.text_input("Nome do Autor", value=default_values.get("author_name", ""))
        author_address = st.text_input("Endereço do Autor", value=default_values.get("author_address", ""))
        author_nif = st.text_input("NIF do Autor", value=default_values.get("author_nif", ""))
        oa_number = st.text_input("Número de Registo na Ordem dos Arquitectos", value=default_values.get("oa_number", ""))
        oa_ref_number = st.text_input("Código de validação para verificação de competências", value=default_values.get("oa_ref_number", ""))
        location = st.text_input("Localização", value=default_values.get("location", ""))
    
    # Build variables dictionary
    variables = {
        "author_name": author_name,
        "author_address": author_address,
        "author_nif": author_nif,
        "construction_type": construction_type,
        "construction_address": construction_address,
        "property_description": property_description,
        "request_type": request_type,
        "requester_name": requester_name,
        "requester_role": requester_role,
        "requester_nif": requester_nif,
        "requester_address": requester_address,
        "location": location,
        "land_registry_location": land_registry_location,
        "land_registry_number": land_registry_number,
        "land_registry_sublocation": land_registry_sublocation,
        "oa_number": oa_number,
        "oa_ref_number": oa_ref_number,
        "regulatory_reference": regulatory_reference,
        "pdm": pdm,
        "qty": str(qty),
        "cost_per_unit": str(cost_per_unit),
        "technical_information_id": technical_information_id,
        "process_nr": process_nr,
        "table_row1": table_row1,
        "table_row2": table_row2,
        "table_row3": table_row3,
        "table_row4": table_row4,
        "table_row5": table_row5,
        "table_row6": table_row6,
        "table_row7": table_row7,
        "table_row8": table_row8,
        "table_row9": table_row9,
        "table_row10": table_row10,
        "table_row11": table_row11,
        "table_row12": table_row12,
        "table_row13": table_row13,
        "table_row14": table_row14,
        "table_row15": table_row15,
        "table_row16": table_row16,
        "table_row17": table_row17,
        "table_row18": table_row18,
        "table_row19": table_row19,
        "table_row20": table_row20
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
        page_title="ArchiDocs",
        page_icon="📄",
        layout="wide"
    )
    
    # Add CSS to make button text smaller
    st.write('<style>div.stButton button p { font-size: 0.8rem !important; }</style>', unsafe_allow_html=True)
    
    # Use built-in anchor=False parameter to remove links from headers
    st.title("ArchiDocs", anchor=False)
    st.write("Cria todos os documentos necessários para o teu projecto de arquitetura com um clique")
    
    # Get available templates
    try:
        template_list = get_templates()
        if not template_list:
            st.warning("No templates found. Please contact customer support.")
    except Exception as e:
        st.error(f"Error loading templates: {str(e)}")
        template_list = []
    
    # Sidebar for actions and template selection
    with st.sidebar:
        st.header("Opções", anchor=False)
        
        # Load/save variables
        if st.button("Carregar valores padrão", use_container_width=True):
            st.session_state.variables = load_default_variables()
            st.success("Valores carregados!")
            
        if st.button("Guardar valores", use_container_width=True):
            if "variables" in st.session_state:
                save_variables(st.session_state.variables)
            else:
                st.error("No variables to save.")
        
        # Template selection
        st.header("Criar documentos", anchor=False)
        if template_list:
            selected_template = st.selectbox(
                "Selecionar modelo",
                options=template_list
            )
            
            # Generate buttons stacked vertically instead of columns
            if st.button("Criar documento selecionado", use_container_width=True):
                if "variables" in st.session_state:
                    with st.spinner("A criar documento..."):
                        result = generate_document_from_dict(
                            selected_template,
                            st.session_state.variables
                        )
                        if result.success:
                            st.success(f"Documento criado com sucesso!")
                            # List the files with download buttons
                            st.write("Documentos criados:")
                            col1, col2 = st.columns([0.9, 0.1])
                            with col1:
                                st.write(f"- {os.path.basename(result.file_path)}")
                            with col2:
                                # Add download button
                                with open(result.file_path, "rb") as file:
                                    st.download_button(
                                        label="↓",
                                        data=file,
                                        file_name=os.path.basename(result.file_path),
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key=f"download_single_{os.path.basename(result.file_path)}"
                                    )
                        else:
                            st.error(f"Erro: {result.error_message}")
                else:
                    st.error("Por favor, preencha o formulário primeiro.")
            
            if st.button("Criar todos os documentos", use_container_width=True):
                if "variables" in st.session_state:
                    with st.spinner("A criar todos os documentos..."):
                        results = generate_document_from_dict(
                            selected_template,
                            st.session_state.variables,
                            generate_all=True
                        )
                        success_count = sum(1 for r in results if r.success)
                        if success_count > 0:
                            st.success(f"{success_count} documentos criados com sucesso!")
                            # List the files with download buttons
                            st.write("Documentos criados:")
                            for result in results:
                                if result.success:
                                    col1, col2 = st.columns([0.9, 0.1])
                                    with col1:
                                        st.write(f"- {os.path.basename(result.file_path)}")
                                    with col2:
                                        # Add download button
                                        with open(result.file_path, "rb") as file:
                                            st.download_button(
                                                label="↓",
                                                data=file,
                                                file_name=os.path.basename(result.file_path),
                                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                key=f"download_{os.path.basename(result.file_path)}"
                                            )
                        else:
                            st.error("Falha ao criar os documentos.")
                else:
                    st.error("Por favor, preencha o formulário primeiro.")
    
    # Main form area
    if "variables" not in st.session_state:
        st.session_state.variables = load_default_variables()
    
    # Use st.subheader for a smaller header
    st.subheader("Adicionar informações para documentos aqui", anchor=False)
    updated_variables = display_document_form(st.session_state.variables)
    
    # Update session state when form is submitted
    if st.button("Atualizar valores", use_container_width=True):
        st.session_state.variables = updated_variables
        st.success("Valores atualizados!")


if __name__ == "__main__":
    main() 