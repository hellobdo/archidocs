"""
Document Generation Application - Main Entry Point

This file serves as a simple entry point to launch the Streamlit UI.
"""
import os
import subprocess
import sys

def main():
    """Launch the Streamlit frontend app."""
    # Get the full path to the frontend app.py file
    frontend_app_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "frontend", 
        "app.py"
    )
    
    # Run Streamlit with our frontend app
    subprocess.run([
        "streamlit", 
        "run", 
        frontend_app_path,
        "--server.maxUploadSize=50",  # Allow larger file uploads (in MB)
    ])

if __name__ == "__main__":
    main() 