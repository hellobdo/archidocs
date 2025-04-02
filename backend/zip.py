import os
import zipfile
from typing import List, Optional

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