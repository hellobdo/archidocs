from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import html
import os
import argparse
import sys

def rgb_to_hex(rgb):
    """Convert RGB color to hex."""
    return '#{:02x}{:02x}{:02x}'.format(rgb.red, rgb.green, rgb.blue)

def get_paragraph_style(paragraph):
    """Extract style information from a paragraph."""
    style = {}
    
    # Font properties
    if paragraph.style.font.size:
        style['font-size'] = f"{paragraph.style.font.size.pt}pt"
    if paragraph.style.font.name:
        style['font-family'] = f"'{paragraph.style.font.name}'"
    if paragraph.style.font.bold:
        style['font-weight'] = 'bold'
    if paragraph.style.font.italic:
        style['font-style'] = 'italic'
    
    # Paragraph properties
    if paragraph.paragraph_format.alignment:
        alignment_map = {
            WD_ALIGN_PARAGRAPH.LEFT: 'left',
            WD_ALIGN_PARAGRAPH.CENTER: 'center',
            WD_ALIGN_PARAGRAPH.RIGHT: 'right',
            WD_ALIGN_PARAGRAPH.JUSTIFY: 'justify'
        }
        style['text-align'] = alignment_map.get(paragraph.paragraph_format.alignment, 'left')
    
    if paragraph.paragraph_format.space_after:
        style['margin-bottom'] = f"{paragraph.paragraph_format.space_after.pt}pt"
    
    if paragraph.paragraph_format.space_before:
        style['margin-top'] = f"{paragraph.paragraph_format.space_before.pt}pt"
    
    return style

def style_to_css(style_name, properties):
    """Convert style properties to CSS rule."""
    css_properties = [f"    {key}: {value};" for key, value in properties.items()]
    return f".{style_name} {{\n" + "\n".join(css_properties) + "\n}"

def docx_to_html_css(docx_path):
    """Convert DOCX file to HTML and CSS."""
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"DOCX file not found: {docx_path}")
        
    doc = Document(docx_path)
    html_parts = ['<!DOCTYPE html>', '<html lang="pt">', '<head>', 
                  '<meta charset="UTF-8">', 
                  '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                  '<title>Plano de Acessibilidades</title>',
                  '<link rel="stylesheet" href="styles.css">',
                  '</head>', '<body>', '<div class="container">']
    
    css_rules = []
    used_styles = set()
    
    # Process document content
    for i, paragraph in enumerate(doc.paragraphs):
        if not paragraph.text.strip():
            continue
            
        style_name = f"p{i}"
        style_props = get_paragraph_style(paragraph)
        used_styles.add(style_name)
        
        # Convert paragraph to HTML
        html_content = []
        for run in paragraph.runs:
            text = html.escape(run.text)
            if run.bold:
                text = f"<strong>{text}</strong>"
            if run.italic:
                text = f"<em>{text}</em>"
            html_content.append(text)
            
        html_parts.append(f'<p class="{style_name}">{"".join(html_content)}</p>')
        css_rules.append(style_to_css(style_name, style_props))
    
    # Close HTML tags
    html_parts.extend(['</div>', '</body>', '</html>'])
    
    # Base CSS
    base_css = """
/* Base styles */
body {
    font-family: 'Century Gothic', sans-serif;
    line-height: 1.6;
    margin: 40px;
    color: #000000;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Century Gothic', sans-serif;
    margin-bottom: 1em;
}

/* Accessibility specific styles */
.accessibility-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 20px;
}

.title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Content sections */
.section {
    margin-bottom: 2em;
}

/* Lists */
ul, ol {
    padding-left: 2em;
    margin-bottom: 1em;
}

/* Links */
a {
    color: #4472c4;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
"""
    
    # Combine base CSS with document-specific rules
    css_content = base_css + "\n\n" + "\n\n".join(css_rules)
    
    return "\n".join(html_parts), css_content

def save_output(html_content, css_content, output_dir, filename_base):
    """Save HTML and CSS files."""
    os.makedirs(output_dir, exist_ok=True)
    
    html_file = os.path.join(output_dir, f'{filename_base}.html')
    css_file = os.path.join(output_dir, 'styles.css')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
        
    return html_file, css_file

def main():
    parser = argparse.ArgumentParser(description='Convert DOCX file to HTML and CSS')
    parser.add_argument('docx_file', help='Path to the DOCX file')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory (default: output)')
    
    args = parser.parse_args()
    
    try:
        # Get filename without extension for output
        filename_base = os.path.splitext(os.path.basename(args.docx_file))[0]
        
        # Convert DOCX to HTML and CSS
        html_content, css_content = docx_to_html_css(args.docx_file)
        
        # Save the output files
        html_file, css_file = save_output(html_content, css_content, args.output_dir, filename_base)
        
        print(f"Conversion completed successfully!")
        print(f"HTML file saved as: {html_file}")
        print(f"CSS file saved as: {css_file}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 