#!/usr/bin/env python3
"""
MCP Image Loader Server for LM Studio
Allows the model to load images from files (jpg, png) for analysis.

This script runs as an MCP server and returns images in a format
that LM Studio can display to the model.
"""

import sys
import base64
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from PIL import Image
import io

# Initialize the MCP server
mcp = FastMCP("Image Loader")


@mcp.tool()
def load_image(file_path: str) -> list:
    """
    Load an image file and return it in a format LM Studio can display.
    
    Args:
        file_path: Absolute or relative path to the image file
        
    Returns:
        List containing text info and the image resource
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return [{
            "type": "text",
            "text": f"Error: File not found: {file_path}"
        }]
    
    if not path.is_file():
        return [{
            "type": "text", 
            "text": f"Error: Not a file: {file_path}"
        }]
    
    # Check supported extensions
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    if path.suffix.lower() not in supported_extensions:
        return [{
            "type": "text",
            "text": f"Error: Unsupported file type: {path.suffix}. Supported: {', '.join(supported_extensions)}"
        }]
    
    try:
        # Open and validate image with PIL
        with Image.open(path) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ("RGBA", "P", "LA"):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes as PNG
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
            
            # Encode to base64
            base64_data = base64.b64encode(image_bytes).decode('utf-8')
            
            # Get image info
            width, height = img.size
            file_size = len(image_bytes)
        
        # Return BOTH text info AND the image resource
        return [
            {
                "type": "text",
                "text": f"Successfully loaded image: {path.name}\nDimensions: {width}x{height}\nSize: {file_size:,} bytes"
            },
            {
                "type": "image",
                "data": base64_data,
                "mimeType": "image/png"
            }
        ]
        
    except Exception as e:
        return [{
            "type": "text",
            "text": f"Error loading image: {str(e)}"
        }]


if __name__ == "__main__":
    mcp.run()
