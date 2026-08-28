#!/usr/bin/env python3
"""
Image Loader Tool for LM Studio
Allows the model to load images from files (jpg, png) for analysis.

Usage:
    python image_loader.py <path_to_image>
    
The tool will read the image file and return it as base64-encoded data
that can be used by LM Studio for vision analysis.
"""

import sys
import os
import base64
import json
from pathlib import Path


def get_mime_type(file_path: str) -> str:
    """Determine MIME type based on file extension."""
    ext = Path(file_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
    }
    return mime_types.get(ext, 'application/octet-stream')


def validate_image_file(file_path: str) -> tuple[bool, str]:
    """Validate that the file exists and is a supported image format."""
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return False, f"File not found: {file_path}"
    
    if not path.is_file():
        return False, f"Not a file: {file_path}"
    
    # Check file extension
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    if path.suffix.lower() not in supported_extensions:
        return False, f"Unsupported file type: {path.suffix}. Supported: {', '.join(supported_extensions)}"
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_size = path.stat().st_size
    if file_size > max_size:
        return False, f"File too large: {file_size / (1024*1024):.2f}MB (max 10MB)"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, "OK"


def load_image(file_path: str) -> dict:
    """
    Load an image file and return it as base64-encoded data.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Dictionary with status, message, and optionally image_data
    """
    # Validate the file
    is_valid, message = validate_image_file(file_path)
    if not is_valid:
        return {
            "success": False,
            "error": message,
            "image_data": None
        }
    
    try:
        # Read the file
        with open(file_path, 'rb') as f:
            image_bytes = f.read()
        
        # Encode to base64
        base64_data = base64.b64encode(image_bytes).decode('utf-8')
        
        # Get MIME type
        mime_type = get_mime_type(file_path)
        
        # Create data URI
        data_uri = f"data:{mime_type};base64,{base64_data}"
        
        # Get file info
        file_info = {
            "filename": os.path.basename(file_path),
            "path": os.path.abspath(file_path),
            "size_bytes": len(image_bytes),
            "mime_type": mime_type,
        }
        
        return {
            "success": True,
            "message": "Image loaded successfully",
            "image_data": data_uri,
            "base64_raw": base64_data,
            "file_info": file_info
        }
        
    except PermissionError:
        return {
            "success": False,
            "error": f"Permission denied: {file_path}",
            "image_data": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error loading image: {str(e)}",
            "image_data": None
        }


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python image_loader.py <path_to_image>",
            "image_data": None
        }, indent=2))
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = load_image(image_path)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
